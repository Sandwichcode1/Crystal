import json
import os
from discord.ext import commands
import discord

class AutoModListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.banned_words_file = "banned_words.json"
        self.status_file = "automod_status.json"

        for file in [self.banned_words_file, self.status_file]:
            if not os.path.exists(file):
                with open(file, "w") as f:
                    json.dump({}, f)

    def _load_words(self):
        with open(self.banned_words_file, "r") as f:
            return json.load(f)

    def _load_status(self):
        with open(self.status_file, "r") as f:
            return json.load(f)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return

        guild_id = str(message.guild.id)
        status_data = self._load_status()
        words_data = self._load_words()

        # Check if automod is enabled
        if not status_data.get(guild_id, {}).get("enabled", True):
            return

        banned_words = words_data.get(guild_id, [])
        message_content = message.content.lower()

        if any(bad_word.lower() in message_content for bad_word in banned_words):
            try:
                await message.delete()
                await message.channel.send(
                    f"🚫 {message.author.mention}, your message contained a banned word.",
                    delete_after=5
                )
            except discord.Forbidden:
                pass  # Missing permissions to delete or send
            except Exception as e:
                print(f"[AutoMod Error] {e}")

async def setup(bot):
    await bot.add_cog(AutoModListener(bot))
