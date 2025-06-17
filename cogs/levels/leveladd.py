# cogs/levels/level_add.py
import discord, json, os
from discord.ext import commands
from discord import app_commands
class LevelAdd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file_path = "cogs/level_data.json"
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump({}, f)

    @app_commands.command(name="leveladd", description="Add level to a user")
    async def leveladd(self, ctx: commands.Context, user: discord.Member, amount: int):
        if not ctx.author.guild_permissions.manage_guild:
            return await ctx.send("❌ You don't have permission to use this command.", ephemeral=True)

        with open(self.file_path, "r") as f:
            data = json.load(f)

        uid = str(user.id)
        data.setdefault(uid, {"level": 0})
        data[uid]["level"] += amount

        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

        await ctx.send(f"✅ Added `{amount}` level(s) to {user.mention}.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(LevelAdd(bot))
