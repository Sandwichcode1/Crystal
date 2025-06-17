import json
import os
from discord.ext import commands
from discord import app_commands
import discord

class AutomodRemoveWord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.banned_words_file = "banned_words.json"
        if not os.path.exists(self.banned_words_file):
            with open(self.banned_words_file, "w") as f:
                json.dump({}, f)

    def _load_words(self):
        with open(self.banned_words_file, "r") as f:
            return json.load(f)

    def _save_words(self, data):
        with open(self.banned_words_file, "w") as f:
            json.dump(data, f, indent=4)

    async def has_staff_permission(self, interaction: discord.Interaction) -> bool:
        return interaction.user.guild_permissions.manage_guild

    @app_commands.command(name="automod_remove_word", description="Remove a banned word for this server")
    @app_commands.describe(word="Word to remove")
    async def automod_remove_word(self, interaction: discord.Interaction, word: str):
        if not await self.has_staff_permission(interaction):
            await interaction.response.send_message(
                "❌ You don't have permission to use this command.", ephemeral=True
            )
            return

        data = self._load_words()
        guild_id = str(interaction.guild_id)

        if guild_id not in data or word.lower() not in [w.lower() for w in data[guild_id]]:
            msg = f"⚠️ The word **{word}** is not in the banned list."
        else:
            data[guild_id] = [w for w in data[guild_id] if w.lower() != word.lower()]
            self._save_words(data)
            msg = f"✅ Removed **{word}** from banned words for this server."

        await interaction.response.send_message(msg, ephemeral=True)

async def setup(bot):
    await bot.add_cog(AutomodRemoveWord(bot))
