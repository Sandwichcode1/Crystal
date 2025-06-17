import discord
import json
import os
from discord.ext import commands
from discord import app_commands

STAFF_FILE = "cogs/staff_roles.json"

class SetStaffRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not os.path.exists(STAFF_FILE):
            with open(STAFF_FILE, "w") as f:
                json.dump({}, f)
    ()
    @app_commands.command(name="setstaffrole", description="Set the staff role for this server")
    @app_commands.describe(role="Role to set as staff")
    async def setstaffrole(self, ctx: discord.interactions, role: discord.Role):
        if not ctx.user.guild_permissions.administrator:
            await ctx.response.send_message("❌ You need administrator permissions.", ephemeral=True)
            return

        with open(STAFF_FILE, "r") as f:
            data = json.load(f)

        data[str(ctx.guild.id)] = role.id

        with open(STAFF_FILE, "w") as f:
            json.dump(data, f, indent=4)

        await ctx.response.send_message(f"✅ Staff role set to {role.mention}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(SetStaffRole(bot))
