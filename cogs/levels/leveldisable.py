import discord
from discord.ext import commands
from discord import app_commands

class LevelDisable(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.leveling_enabled = True

    @app_commands.command(name="leveldisable", description="Disable the leveling system.")
    async def leveldisable(self, interaction: discord.Interaction):
        self.leveling_enabled = False
        await interaction.response.send_message("⛔ Leveling system disabled.")

async def setup(bot):
    await bot.add_cog(LevelDisable(bot))
