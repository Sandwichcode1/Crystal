import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import random
import json
import os

GIVEAWAYS_FILE = "cogs/giveaways.json"

class GiveawayManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.giveaways = {}  # message_id: giveaway_data
        if os.path.exists(GIVEAWAYS_FILE):
            with open(GIVEAWAYS_FILE, "r") as f:
                self.giveaways = json.load(f)
        else:
            self._save_giveaways()

    def _save_giveaways(self):
        with open(GIVEAWAYS_FILE, "w") as f:
            json.dump(self.giveaways, f, indent=4)

    async def _end_giveaway(self, message_id: str):
        giveaway = self.giveaways.get(message_id)
        if not giveaway:
            return False, "Giveaway not found."

        channel = self.bot.get_channel(giveaway["channel_id"])
        if not channel:
            return False, "Channel not found."

        try:
            message = await channel.fetch_message(int(message_id))
        except Exception:
            return False, "Giveaway message not found."

        users = []
        for reaction in message.reactions:
            if str(reaction.emoji) == giveaway["emoji"]:
                users = await reaction.users().flatten()
                break

        users = [u for u in users if not u.bot]

        winners_count = giveaway.get("winners", 1)
        if len(users) < winners_count:
            winners = users
        else:
            winners = random.sample(users, winners_count)

        winner_mentions = ", ".join(w.mention for w in winners) if winners else "No valid entrants."
        embed = discord.Embed(
            title="🎉 Giveaway Ended! 🎉",
            description=f"Prize: **{giveaway['prize']}**\nWinners: {winner_mentions}",
            color=discord.Color.green()
        )
        await channel.send(embed=embed)

        self.giveaways.pop(message_id)
        self._save_giveaways()
        return True, None

    @app_commands.command(name="giveaway_start")
    @app_commands.describe(duration="Duration in seconds", prize="Prize to giveaway", winners="Number of winners (default 1)")
    async def giveaway_start(self, interaction: discord.Interaction, duration: int, prize: str, winners: int = 1):
        embed = discord.Embed(
            title="🎉 Giveaway Started! 🎉",
            description=f"Prize: **{prize}**\nReact with 🎉 to enter!\nDuration: {duration} seconds\nWinners: {winners}",
            color=discord.Color.gold()
        )
        message = await interaction.channel.send(embed=embed)
        await message.add_reaction("🎉")

        self.giveaways[str(message.id)] = {
            "channel_id": interaction.channel.id,
            "prize": prize,
            "winners": winners,
            "start_time": interaction.created_at.timestamp(),
            "duration": duration,
            "emoji": "🎉"
        }
        self._save_giveaways()

        await interaction.response.send_message(f"✅ Giveaway started! [Jump to message]({message.jump_url})", ephemeral=True)

        await asyncio.sleep(duration)
        if str(message.id) in self.giveaways:
            ended, err = await self._end_giveaway(str(message.id))
            if ended:
                try:
                    await interaction.channel.send("Giveaway ended automatically.")
                except:
                    pass

    @app_commands.command(name="giveaway_end")
    @app_commands.describe(message_id="Message ID of the giveaway to end")
    async def giveaway_end(self, interaction: discord.Interaction, message_id: int):
        ended, error = await self._end_giveaway(str(message_id))
        if ended:
            await interaction.response.send_message("✅ Giveaway ended successfully.", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ {error}", ephemeral=True)

    @app_commands.command(name="giveaway_reroll")
    @app_commands.describe(message_id="Message ID of the giveaway to reroll")
    async def giveaway_reroll(self, interaction: discord.Interaction, message_id: int):
        giveaway = self.giveaways.get(str(message_id))
        if not giveaway:
            return await interaction.response.send_message("❌ Giveaway not found.", ephemeral=True)

        channel = self.bot.get_channel(giveaway["channel_id"])
        if not channel:
            return await interaction.response.send_message("❌ Giveaway channel not found.", ephemeral=True)

        try:
            message = await channel.fetch_message(message_id)
        except Exception:
            return await interaction.response.send_message("❌ Giveaway message not found.", ephemeral=True)

        users = []
        for reaction in message.reactions:
            if str(reaction.emoji) == giveaway["emoji"]:
                users = await reaction.users().flatten()
                break

        users = [u for u in users if not u.bot]

        winners_count = giveaway.get("winners", 1)
        if len(users) < winners_count:
            winners = users
        else:
            winners = random.sample(users, winners_count)

        winner_mentions = ", ".join(w.mention for w in winners) if winners else "No valid entrants."
        await interaction.response.send_message(f"🎉 New winner(s): {winner_mentions}", ephemeral=True)

    @app_commands.command(name="giveaway_list")
    async def giveaway_list(self, interaction: discord.Interaction):
        if not self.giveaways:
            return await interaction.response.send_message("No active giveaways.", ephemeral=True)
        lines = []
        for msg_id, giveaway in self.giveaways.items():
            lines.append(f"Message ID: {msg_id} | Prize: {giveaway['prize']} | Winners: {giveaway.get('winners',1)}")
        await interaction.response.send_message("\n".join(lines), ephemeral=True)

    @app_commands.command(name="giveaway_info")
    @app_commands.describe(message_id="Message ID of giveaway to view info")
    async def giveaway_info(self, interaction: discord.Interaction, message_id: int):
        giveaway = self.giveaways.get(str(message_id))
        if not giveaway:
            return await interaction.response.send_message("Giveaway not found.", ephemeral=True)
        channel = self.bot.get_channel(giveaway["channel_id"])
        embed = discord.Embed(title="Giveaway Info", color=discord.Color.blue())
        embed.add_field(name="Prize", value=giveaway["prize"], inline=False)
        embed.add_field(name="Winners", value=str(giveaway.get("winners", 1)), inline=False)
        embed.add_field(name="Channel", value=channel.mention if channel else "Unknown", inline=False)
        embed.add_field(name="Duration (s)", value=str(giveaway["duration"]), inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="giveaway_cancel")
    @app_commands.describe(message_id="Message ID of the giveaway to cancel")
    async def giveaway_cancel(self, interaction: discord.Interaction, message_id: int):
        if str(message_id) not in self.giveaways:
            return await interaction.response.send_message("Giveaway not found.", ephemeral=True)
        self.giveaways.pop(str(message_id))
        self._save_giveaways()
        await interaction.response.send_message("Giveaway cancelled successfully.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(GiveawayManager(bot))
