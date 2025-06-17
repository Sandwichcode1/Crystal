import discord
from discord.ext import commands
from discord import app_commands

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    ()
    @app_commands.command(name="kick", description="Kick a user from the server")
    @app_commands.describe(user="User to kick", reason="Reason for kicking")
    async def kick(self, ctx: discord.interactions, user: discord.Member, reason: str = None):
        if not ctx.user.guild_permissions.kick_members:
            await ctx.response.send_message("You do not have permission to kick members.", ephemeral=True)
            return
        try:
            await user.kick(reason=reason)
            await ctx.response.send_message(f"Kicked {user.display_name} from the server.")
        except discord.Forbidden:
            await ctx.response.send_message("I don't have permission to kick that user.", ephemeral=True)
        except Exception as e:
            await ctx.response.send_message(f"Failed to kick user: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Kick(bot))
