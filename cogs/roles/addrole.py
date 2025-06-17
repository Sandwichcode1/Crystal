import discord
from discord.ext import commands
from discord import app_commands

class AddRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    ()
    @app_commands.command(name="addrole", description="Add a role to a user")
    @app_commands.describe(user="User to add the role to", role="Role to add")
    async def addrole(self, ctx: discord.interactions, user: discord.Member, role: discord.Role):
        if not ctx.user.guild_permissions.manage_roles:
            await ctx.response.send_message("You do not have permission to manage roles.", ephemeral=True)
            return
        try:
            await user.add_roles(role)
            await ctx.response.send_message(f"Added role {role.name} to {user.display_name}.")
        except discord.Forbidden:
            await ctx.response.send_message("I don't have permission to add that role.", ephemeral=True)
        except Exception as e:
            await ctx.response.send_message(f"Failed to add role: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(AddRole(bot))
