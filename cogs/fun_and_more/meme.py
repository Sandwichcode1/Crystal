import discord
from discord.ext import commands
import aiohttp
from discord import app_commands
class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="meme", description="Get a random meme.")
    async def meme(self, ctx: commands.Context):
        url = "https://meme-api.com/gimme"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await ctx.response.send_message("Could not fetch meme.", ephemeral=True)
                data = await resp.json()
                embed = discord.Embed(title=data.get('title', 'Meme'))
                embed.set_image(url=data.get('url', ''))
                await ctx.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Meme(bot))
