import discord
from discord.ext import commands
from discord import app_commands
import traceback
import textwrap
import io
import contextlib

class Eval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    ()
    @app_commands.command(name="eval", description="Evaluate python code (owner only).")
    @app_commands.describe(code="Python code to evaluate")
    async def eval(self, ctx: discord.interactions, code: str):
        if ctx.user.id != 976469246936756246:  # Replace YOUR_USER_ID with your Discord ID
            return await ctx.response.send_message("You are not authorized to use this command.", ephemeral=True)

        code = code.strip("` ")
        local_vars = {
            "discord": discord,
            "commands": commands,
            "bot": self.bot,
            "ctx": ctx,
        }
        stdout = io.StringIO()
        try:
            with contextlib.redirect_stdout(stdout):
                exec(
                    f"async def func():\n{textwrap.indent(code, '    ')}", local_vars
                )
                func = local_vars["func"]
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.response.send_message(f"```py\n{value}{traceback.format_exc()}```")
        else:
            value = stdout.getvalue()
            if ret is None:
                if value:
                    await ctx.response.send_message(f"```py\n{value}```")
                else:
                    await ctx.response.send_message("No output.")
            else:
                await ctx.response.send_message(f"```py\n{value}{ret}```")

async def setup(bot):
    await bot.add_cog(Eval(bot))
