from discord.ext import commands
from discord import app_commands
import discord
YOUR_DEV_ID = 976469246936756246  # Replace with your Discord user ID

class Shutdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="shutdown", description="Shut down the bot")
    async def shutdown(self, interaction: discord.Interaction):
        if interaction.user.id != YOUR_DEV_ID:
            return await interaction.response.send_message("❌ You can't use this command.", ephemeral=True)
        await interaction.response.send_message("🛑 Shutting down...", ephemeral=True)
        await self.bot.close()

async def setup(bot):
    await bot.add_cog(Shutdown(bot))
