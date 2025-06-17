import discord
from discord.ext import commands
import random
from discord import app_commands
class Coinflip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="coinflip", description="Flip a coin.")
    async def coinflip(self, ctx: commands.Context):
        result = random.choice(["Heads", "Tails"])
        await ctx.response.send_message(f"🪙 The coin landed on **{result}**!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Coinflip(bot))
