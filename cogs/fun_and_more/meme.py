import discord
from discord.ext import commands
from discord import app_commands
import aiohttp

class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="meme", description="Get a random meme.")
    async def meme(self, interaction: discord.Interaction):
        url = "https://meme-api.com/gimme"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await interaction.response.send_message("Could not fetch meme.")
                data = await resp.json()
                embed = discord.Embed(title=data['title'])
                embed.set_image(url=data['url'])
                await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Meme(bot))
