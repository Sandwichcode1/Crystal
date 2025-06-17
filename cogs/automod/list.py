import json
import os
from discord.ext import commands
from discord import app_commands
import discord

class AutomodList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.banned_words_file = "banned_words.json"
        if not os.path.exists(self.banned_words_file):
            with open(self.banned_words_file, "w") as f:
                json.dump({}, f)

    def _load_words(self):
        with open(self.banned_words_file, "r") as f:
            return json.load(f)

    @app_commands.command(name="automod_list", description="List all banned words for this server")
    @app_commands.guild_only()
    async def automod_list(self, interaction: discord.Interaction):
        data = self._load_words()
        guild_id = str(interaction.guild_id)
        words = data.get(guild_id, [])

        if not words:
            await interaction.response.send_message("📄 No banned words set for this server.", ephemeral=True)
        else:
            await interaction.response.send_message("📄 Banned words: " + ", ".join(words), ephemeral=True)

async def setup(bot):
    await bot.add_cog(AutomodList(bot))
    # Sync commands for all guilds (or globally)
    try:
        await bot.tree.sync()
        print("Slash commands synced successfully.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

async def setup(bot):
    await bot.add_cog(AutomodList(bot))
