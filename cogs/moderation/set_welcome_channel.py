import discord
from discord.ext import commands
from discord import app_commands

class SetWelcomeChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_channel_id = None  # Store channel id; use persistent storage for real bots

    @app_commands.command(name="set-welcome-channel", description="Set the welcome channel.")
    @app_commands.describe(channel="The channel to send welcome messages")
    async def set_welcome_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        self.welcome_channel_id = channel.id
        await interaction.response.send_message(f"✅ Welcome channel set to {channel.mention}")

async def setup(bot):
    await bot.add_cog(SetWelcomeChannel(bot))
