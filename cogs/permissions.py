# cogs/utils/permissions.py
import json
import os
import discord
from functools import wraps

STAFF_FILE = "cogs/staff_roles.json"

def load_staff_roles():
    if not os.path.exists(STAFF_FILE):
        with open(STAFF_FILE, "w") as f:
            json.dump({}, f)
    with open(STAFF_FILE, "r") as f:
        return json.load(f)

def get_staff_role_id(guild_id):
    roles = load_staff_roles()
    return roles.get(str(guild_id))

def has_staff_role(member: discord.Member) -> bool:
    role_id = get_staff_role_id(member.guild.id)
    return any(role.id == role_id for role in member.roles) if role_id else False

def staff_only():
    def decorator(func):
        @wraps(func)
        async def wrapper(self, ctx: discord.interactions, *args, **kwargs):
            if not has_staff_role(ctx.user):
                await ctx.response.send_message("❌ You must be a staff member to use this command.", ephemeral=True)
                return
            return await func(self, ctx, *args, **kwargs)
        return wrapper
    return decorator
