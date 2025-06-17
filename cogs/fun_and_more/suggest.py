import discord
from discord.ext import commands
from discord import app_commands
import json
import os

SUGGESTION_CHANNEL_NAME = "suggestions"
SUGGESTION_FILE = "suggestions.json"

class Suggest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not os.path.exists(SUGGESTION_FILE):
            with open(SUGGESTION_FILE, "w") as f:
                json.dump({}, f)

    def save_suggestion(self, guild_id: int, user: discord.User, suggestion: str):
        with open(SUGGESTION_FILE, "r") as f:
            data = json.load(f)

        guild_key = str(guild_id)
        if guild_key not in data:
            data[guild_key] = []

        data[guild_key].append({
            "user": str(user),
            "user_id": user.id,
            "suggestion": suggestion
        })

        with open(SUGGESTION_FILE, "w") as f:
            json.dump(data, f, indent=4)

    async def get_or_create_suggestion_channel(self, guild: discord.Guild):
        channel = discord.utils.get(guild.text_channels, name=SUGGESTION_CHANNEL_NAME)
        if channel is None:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            try:
                channel = await guild.create_text_channel(
                    SUGGESTION_CHANNEL_NAME,
                    overwrites=overwrites,
                    reason="Created suggestion channel for suggestions command"
                )
            except discord.Forbidden:
                return None
        return channel

    @app_commands.command(name="suggest", description="Send a suggestion.")
    @app_commands.describe(suggestion="Your suggestion")
    async def suggest(self, interaction: discord.Interaction, suggestion: str):
        channel = await self.get_or_create_suggestion_channel(interaction.guild)
        if channel is None:
            return await interaction.response.send_message(
                "❌ I don't have permission to create or access the suggestions channel.", ephemeral=True
            )

        embed = discord.Embed(
            title="📬 New Suggestion",
            description=suggestion,
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow()
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)

        try:
            await channel.send(embed=embed)
            self.save_suggestion(interaction.guild.id, interaction.user, suggestion)
            await interaction.response.send_message("✅ Your suggestion has been sent and saved!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to send suggestion: {e}", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Suggest(bot))
