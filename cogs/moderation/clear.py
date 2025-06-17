import discord
from discord.ext import commands
from discord import app_commands

# Reusable permission check for mods/admins
def is_moderator():
    async def predicate(ctx: discord.interactions):
        perms = ctx.user.guild_permissions
        return perms.manage_messages or perms.administrator
    return app_commands.check(predicate)

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    ()
    @app_commands.command(name="clear", description="Delete a number of messages.")
    @app_commands.describe(amount="Number of messages to delete.")
    @is_moderator()
    async def clear(self, ctx: discord.interactions, amount: int):
        # Defer to avoid timeout
        await ctx.response.defer(ephemeral=True)

        # Try to purge messages
        try:
            deleted = await ctx.channel.purge(limit=amount)
            await ctx.followup.send(f"🧹 Deleted {len(deleted)} messages.", ephemeral=True)
        except discord.Forbidden:
            await ctx.followup.send("❌ I don't have permission to delete messages.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Clear(bot))
