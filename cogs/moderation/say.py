import discord
from discord.ext import commands
from discord import app_commands

# Permission check: Only users with Manage Messages or Administrator can use the command
def is_moderator():
    async def predicate(ctx: discord.interactions):
        perms = ctx.user.guild_permissions
        return perms.manage_messages or perms.administrator
    return app_commands.check(predicate)

class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    ()
    @app_commands.command(name="say", description="Make the bot say something.")
    @app_commands.describe(message="The message to say")
    @is_moderator()
    async def say(self, ctx: discord.interactions, message: str):
        await ctx.response.send_message(message)

async def setup(bot):
    await bot.add_cog(Say(bot))
