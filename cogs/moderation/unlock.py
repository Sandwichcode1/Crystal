import discord
from discord.ext import commands
from discord import app_commands

class Unlock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="unlock", description="Unlock the current channel.")
    async def unlock(self, interaction: discord.Interaction):
        overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = None
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.response.send_message("🔓 Channel unlocked.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Unlock(bot))
