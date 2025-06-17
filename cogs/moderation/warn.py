import discord
from discord.ext import commands
from discord import app_commands
import json
import os

WARN_FILE = "warns.json"

def load_warns():
    if not os.path.exists(WARN_FILE):
        with open(WARN_FILE, "w") as f:
            json.dump({}, f)
    with open(WARN_FILE, "r") as f:
        return json.load(f)

def save_warns(data):
    with open(WARN_FILE, "w") as f:
        json.dump(data, f, indent=4)

class WarnSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    ()
    @app_commands.command(name="warn", description="Warn a user")
    @app_commands.describe(user="User to warn", reason="Reason for the warning")
    async def warn(self, ctx: discord.interactions, user: discord.User, reason: str):
        warns = load_warns()
        guild_id = str(ctx.guild_id)
        user_id = str(user.id)

        warns.setdefault(guild_id, {}).setdefault(user_id, []).append(reason)
        save_warns(warns)

        await ctx.response.send_message(f"⚠️ {user.mention} has been warned: `{reason}`")
    ()
    @app_commands.command(name="warnlist", description="Show all warnings for a user")
    @app_commands.describe(user="User to view warnings for")
    async def warnlist(self, ctx: discord.interactions, user: discord.User):
        warns = load_warns()
        guild_id = str(ctx.guild_id)
        user_id = str(user.id)

        user_warns = warns.get(guild_id, {}).get(user_id, [])
        if not user_warns:
            await ctx.response.send_message(f"✅ {user.mention} has no warnings.")
            return

        embed = discord.Embed(title=f"Warnings for {user}", color=discord.Color.orange())
        for i, warn in enumerate(user_warns, start=1):
            embed.add_field(name=f"Warning #{i}", value=warn, inline=False)

        await ctx.response.send_message(embed=embed)
    ()
    @app_commands.command(name="removewarn", description="Remove a specific warning from a user")
    @app_commands.describe(user="User to remove a warning from", index="Warning number (1, 2, 3...)")
    async def removewarn(self, ctx: discord.interactions, user: discord.User, index: int):
        warns = load_warns()
        guild_id = str(ctx.guild_id)
        user_id = str(user.id)

        user_warns = warns.get(guild_id, {}).get(user_id, [])
        if not user_warns:
            await ctx.response.send_message(f"❌ {user.mention} has no warnings.")
            return

        if index < 1 or index > len(user_warns):
            await ctx.response.send_message("❌ Invalid warning index.")
            return

        removed = user_warns.pop(index - 1)
        warns[guild_id][user_id] = user_warns
        save_warns(warns)

        await ctx.response.send_message(f"🗑️ Removed warning #{index} from {user.mention}: `{removed}`")

async def setup(bot):
    await bot.add_cog(WarnSystem(bot))
