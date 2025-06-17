import discord
from discord.ext import commands
from discord import app_commands

class Unlock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    ()
    @app_commands.command(name="unlock", description="Unlock the current channel.")
    async def unlock(self, ctx: discord.interactions):
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = None
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.response.send_message("🔓 Channel unlocked.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Unlock(bot))
