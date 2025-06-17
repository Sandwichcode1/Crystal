import discord
from discord.ext import commands
from discord import app_commands

# Custom check to allow only users with manage_channels or admin perms
def is_moderator():
    async def predicate(ctx: discord.interactions):
        perms = ctx.user.guild_permissions
        return perms.manage_channels or perms.administrator
    return app_commands.check(predicate)

class Lock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    ()
    @app_commands.command(name="lock", description="Lock the current channel.")
    @is_moderator()
    async def lock(self, ctx: discord.interactions):
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.response.send_message("🔒 Channel locked.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Lock(bot))
