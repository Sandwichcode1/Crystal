from discord.ext import commands
from discord import app_commands
import os
import sys
import discord 
YOUR_DEV_ID = 976469246936756246  # Replace with your Discord user ID

class RestartCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="restart", description="Restart the bot")
    async def restart(self, interaction: discord.Interaction):
        if interaction.user.id != YOUR_DEV_ID:
            return await interaction.response.send_message("❌ You can't use this command.", ephemeral=True)
        await interaction.response.send_message("🔁 Restarting...", ephemeral=True)
        os.execv(sys.executable, [sys.executable] + sys.argv)

async def setup(bot):
    await bot.add_cog(RestartCog(bot))
