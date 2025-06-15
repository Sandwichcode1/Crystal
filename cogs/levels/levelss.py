import discord
from discord.ext import commands
import json
import os

LEVELS_FILE = "levels.json"

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.users = {}
        self.load_levels()

    def load_levels(self):
        if os.path.exists(LEVELS_FILE):
            with open(LEVELS_FILE, "r") as f:
                self.users = json.load(f)
                # convert keys back to int, json saves as str keys
                self.users = {int(k): v for k, v in self.users.items()}
        else:
            # Create empty file
            with open(LEVELS_FILE, "w") as f:
                json.dump({}, f)

    def save_levels(self):
        with open(LEVELS_FILE, "w") as f:
            # Convert keys to strings for JSON serialization
            json.dump({str(k): v for k, v in self.users.items()}, f, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = message.author.id
        if user_id not in self.users:
            self.users[user_id] = {"xp": 0, "level": 1}

        user_data = self.users[user_id]

        # Add XP
        user_data["xp"] += 10

        # Calculate XP needed for next level
        level = user_data["level"]
        xp_needed = 5 * (level ** 2) + 50 * level + 100

        if user_data["xp"] >= xp_needed:
            user_data["level"] += 1
            user_data["xp"] -= xp_needed
            try:
                await message.author.send(
                    f"🎉 Congrats {message.author.mention}, you leveled up to level {user_data['level']}!"
                )
            except discord.Forbidden:
                await message.channel.send(
                    f"🎉 Congrats {message.author.mention}, you leveled up to level {user_data['level']}!"
                )

        self.save_levels()

    @commands.command()
    async def level(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        user_id = member.id
        if user_id not in self.users:
            await ctx.send(f"{member.display_name} has no XP yet.")
            return
        user_data = self.users[user_id]
        await ctx.send(
            f"{member.display_name} is level {user_data['level']} with {user_data['xp']} XP."
        )

async def setup(bot):
    await bot.add_cog(Leveling(bot))
