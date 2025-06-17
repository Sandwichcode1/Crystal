import json
import os
from discord.ext import commands
from discord import app_commands
import discord

class AutomodAddWord(commands.Cog):
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

    @app_commands.command(name="automod_add_word", description="Add a banned word for this server")
    @app_commands.describe(word="Word to ban")
    async def automod_add_word(self, interaction: discord.Interaction, word: str):
        if not await self.has_staff_permission(interaction):
            await interaction.response.send_message(
                "❌ You don't have permission to use this command.", ephemeral=True
            )
            return

        data = self._load_words()
        guild_id = str(interaction.guild_id)

        if guild_id not in data:
            data[guild_id] = []

        if word.lower() in (w.lower() for w in data[guild_id]):
            msg = f"⚠️ The word **{word}** is already banned."
        else:
            data[guild_id].append(word)
            self._save_words(data)
            msg = f"🚫 Added **{word}** to banned words for this server."

        await interaction.response.send_message(msg, ephemeral=True)

async def setup(bot):
    await bot.add_cog(AutomodAddWord(bot))
