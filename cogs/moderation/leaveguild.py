import discord
from discord import app_commands
from discord.ext import commands

class LeaveGuild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="leaveguild", description="Force the bot to leave a server by ID")
    @app_commands.describe(guild_id="The ID of the server to leave")
    async def leave_guild(self, interaction: discord.Interaction, guild_id: str):
        if interaction.user.id != 976469246936756246:  # Replace with your Discord ID
            await interaction.response.send_message("❌ You aren't authorized to use this command.", ephemeral=True)
            return

        guild = self.bot.get_guild(int(guild_id))

        if guild is None:
            await interaction.response.send_message("⚠️ I'm not in a server with that ID.", ephemeral=True)
            return

        try:
            await guild.leave()
            await interaction.response.send_message(f"✅ Left server **{guild.name}** (`{guild.id}`)", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to leave server: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(LeaveGuild(bot))
