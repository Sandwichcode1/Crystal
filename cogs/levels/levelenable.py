import discord
from discord.ext import commands
from discord import app_commands

class LevelEnable(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.leveling_enabled = False

    @app_commands.command(name="levelenable", description="Enable the leveling system.")
    async def levelenable(self, interaction: discord.Interaction):
        self.leveling_enabled = True
        await interaction.response.send_message("✅ Leveling system enabled.")

async def setup(bot):
    await bot.add_cog(LevelEnable(bot))
