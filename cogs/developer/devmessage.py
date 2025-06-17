import discord
from discord.ext import commands
from discord import app_commands

YOUR_DEV_ID = 976469246936756246  # Replace with your Discord user ID

class DevMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="devmessage", description="Send a DM to a user")
    @app_commands.describe(user="User to message", message="Message to send")
    async def devmessage(self, interaction: discord.Interaction, user: discord.User, message: str):
        if interaction.user.id != YOUR_DEV_ID:
            return await interaction.response.send_message("❌ You can't use this command.", ephemeral=True)
        try:
            await user.send(message)
            await interaction.response.send_message("📩 Message sent.", ephemeral=True)
        except Exception:
            await interaction.response.send_message("❌ Could not send message.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(DevMessage(bot))
