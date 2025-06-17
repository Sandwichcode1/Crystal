import discord
from discord.ext import commands
from discord import app_commands
class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Check the bot's latency.")
    async def ping(self, ctx: commands.Context):
        latency = round(self.bot.latency * 1000)
        await ctx.response.send_message(f"Pong! 🏓 Latency: {latency}ms", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Ping(bot))
