import discord
from discord.ext import commands
from discord import app_commands

class Suggest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="suggest", description="Send a suggestion.")
    @app_commands.describe(suggestion="Your suggestion")
    async def suggest(self, interaction: discord.Interaction, suggestion: str):
        # You might want to send this to a specific channel instead
        await interaction.response.send_message(f"💡 Suggestion received:\n{suggestion}")

async def setup(bot):
    await bot.add_cog(Suggest(bot))
