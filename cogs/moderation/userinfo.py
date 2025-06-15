import discord
from discord.ext import commands

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="changeusername", description="Change another user's nickname")
    async def changeusername(self, ctx: commands.Context, user: discord.Member, *, new_nickname: str):
        # Check if command is used in a guild
        if ctx.guild is None:
            await ctx.send("This command can only be used in a server.")
            return

        # Check if bot has permission to manage nicknames
        if not ctx.guild.me.guild_permissions.manage_nicknames:
            await ctx.send("I don't have permission to manage nicknames here.")
            return

        # Check if the command user has permission to manage nicknames (optional)
        if not ctx.author.guild_permissions.manage_nicknames:
            await ctx.send("You don't have permission to manage nicknames.")
            return

        try:
            await user.edit(nick=new_nickname)
            await ctx.send(f"Changed nickname of {user.mention} to: {new_nickname}")
        except discord.Forbidden:
            await ctx.send("I don't have permission to change that user's nickname.")
        except Exception as e:
            await ctx.send(f"Something went wrong: {e}")

async def setup(bot):
    await bot.add_cog(UserInfo(bot))
