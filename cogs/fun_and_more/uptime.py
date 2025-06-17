import discord
from discord.ext import commands
from discord import app_commands
import time

class Uptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    @app_commands.command(name="uptime", description="Shows how long the bot has been online.")
    async def uptime(self, ctx: commands.Context):
        seconds = int(time.time() - self.start_time)
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        await ctx.response.send_message(f"🕒 Uptime: {hours}h {minutes}m {seconds}s", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Uptime(bot))
