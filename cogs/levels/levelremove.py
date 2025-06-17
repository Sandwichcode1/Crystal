# cogs/level_remove.py
import discord
import json
import os
from discord.ext import commands
from discord import app_commands


class LevelRemove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file_path = "cogs/level_data.json"
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump({}, f)

    async def _has_staff_permission(self, ctx):
        return ctx.author.guild_permissions.manage_guild

    @app_commands.command(name="levelremove", description="Remove level(s) from a user.", )
    @app_commands.describe(user="User to remove levels from", amount="Amount of levels to remove")
    async def levelremove(self, ctx: commands.Context, user: discord.Member, amount: int):
        if not await self._has_staff_permission(ctx):
            await ctx.send("❌ You don't have permission to use this command.", ephemeral=True)
            return

        with open(self.file_path, "r") as f:
            data = json.load(f)

        uid = str(user.id)
        data.setdefault(uid, {"level": 0})
        data[uid]["level"] = max(0, data[uid]["level"] - amount)

        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

        await ctx.send(f"🔻 Removed `{amount}` level(s) from {user.mention}.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(LevelRemove(bot))
