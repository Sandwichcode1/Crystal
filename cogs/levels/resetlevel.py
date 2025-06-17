# cogs/reset_level.py
import discord
import json
import os
from discord.ext import commands
from discord import app_commands
class ResetLevel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file_path = "cogs/level_data.json"
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump({}, f)

    @app_commands.command(name="resetlevel", description="Reset a user's level")
    @commands.has_permissions(manage_guild=True)
    async def resetlevel(self, ctx: commands.Context, user: discord.Member):
        with open(self.file_path, "r") as f:
            data = json.load(f)

        uid = str(user.id)
        data[uid] = {"level": 0}

        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

        await ctx.reply(f"🧹 Reset level for {user.mention}.", ephemeral=True if ctx.ctx else False)

async def setup(bot):
    await bot.add_cog(ResetLevel(bot))
