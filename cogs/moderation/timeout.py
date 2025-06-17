import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

class Timeout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    ()
    @app_commands.command(name="timeout", description="Timeout a user for a certain duration")
    @app_commands.describe(user="User to timeout", duration="Duration in minutes", reason="Reason for timeout")
    async def timeout(self, ctx: discord.interactions, user: discord.Member, duration: int, reason: str = None):
        if not ctx.user.guild_permissions.moderate_members:
            await ctx.response.send_message("You do not have permission to timeout members.", ephemeral=True)
            return
        try:
            until = discord.utils.utcnow() + timedelta(minutes=duration)
            await user.edit(timed_out_until=until, reason=reason)
            await ctx.response.send_message(f"Timed out {user.display_name} for {duration} minutes.")
        except discord.Forbidden:
            await ctx.response.send_message("I don't have permission to timeout that user.", ephemeral=True)
        except Exception as e:
            await ctx.response.send_message(f"Failed to timeout user: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Timeout(bot))
