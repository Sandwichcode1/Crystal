import discord
from discord.ext import commands
from discord import app_commands

class RemoveRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="removerole", description="Remove a role from a user")
    @app_commands.describe(user="User to remove the role from", role="Role to remove")
    async def removerole(self, interaction: discord.Interaction, user: discord.Member, role: discord.Role):
        if not interaction.user.guild_permissions.manage_roles:
            await interaction.response.send_message("❌ You do not have permission to manage roles.", ephemeral=True)
            return
        if not interaction.guild.me.top_role > role:
            await interaction.response.send_message("❌ I cannot remove a role higher than my own.", ephemeral=True)
            return
        try:
            await user.remove_roles(role)
            await interaction.response.send_message(f"✅ Removed role **{role.name}** from {user.mention}.")
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to remove that role.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to remove role: `{e}`", ephemeral=True)

async def setup(bot):
    await bot.add_cog(RemoveRole(bot))  # ✅ ONLY this line
