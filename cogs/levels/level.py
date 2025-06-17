import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

XP_FILE = "xp.json"
BACKGROUND_PATH = "cogs/assets/background.png"
FONT_PATH = "cogs/assets/Caprasimo-Regular.ttf"

# Ensure XP file exists
if not os.path.exists(XP_FILE):
    with open(XP_FILE, "w") as f:
        json.dump({}, f)

class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        guild_id = str(message.guild.id)
        user_id = str(message.author.id)

        # Load XP data
        with open(XP_FILE, "r") as f:
            data = json.load(f)

        if guild_id not in data or not data[guild_id].get("enabled", True):
            return  # Exit if leveling is disabled

        if "users" not in data[guild_id]:
            data[guild_id]["users"] = {}

        if user_id not in data[guild_id]["users"]:
            data[guild_id]["users"][user_id] = {"xp": 0, "level": 0}

        user_data = data[guild_id]["users"][user_id]
        user_data["xp"] += 10

        xp = user_data["xp"]
        level = user_data["level"]
        required = (level + 1) * 100

        if xp >= required:
            user_data["level"] += 1
            user_data["xp"] = 0
            try:
                await message.author.send(f"🎉 You leveled up to **{level + 1}**!")
            except discord.Forbidden:
                pass  # User has DMs off

        with open(XP_FILE, "w") as f:
            json.dump(data, f, indent=4)

    @app_commands.command(name="level", description="Check your level.")
    async def level(self, ctx: discord.interactions):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.user.id)

        with open(XP_FILE, "r") as f:
            data = json.load(f)

        if guild_id not in data or not data[guild_id].get("enabled", True):
            await ctx.response.send_message("❌ Leveling is disabled in this server.", ephemeral=True)
            return

        user_data = data[guild_id].get("users", {}).get(user_id, {"xp": 0, "level": 0})
        xp = user_data["xp"]
        level = user_data["level"]
        required = (level + 1) * 100
        progress = xp / required if required > 0 else 0

        image = await self.create_level_card(ctx.user, level, xp, required, progress)
        await ctx.response.send_message(file=image)

    async def create_level_card(self, user, level, xp, required, progress):
        card_width = 500
        card_height = 150

        bg = Image.open(BACKGROUND_PATH).convert("RGBA").resize((card_width, card_height))

        asset = user.display_avatar.with_size(128)
        buffer = BytesIO()
        await asset.save(buffer)
        buffer.seek(0)
        pfp = Image.open(buffer).convert("RGBA").resize((64, 64))

        bg.paste(pfp, (20, 20), pfp)
        draw = ImageDraw.Draw(bg)

        font_big = ImageFont.truetype(FONT_PATH, 24)
        font_small = ImageFont.truetype(FONT_PATH, 18)

        draw.text((100, 20), str(user.name), font=font_big, fill="white")
        draw.text((100, 50), f"Level: {level}", font=font_small, fill="white")
        draw.text((100, 75), f"XP: {xp}/{required}", font=font_small, fill="white")

        bar_x, bar_y = 100, 105
        bar_width, bar_height = 350, 16
        draw.rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + bar_height], fill=(50, 50, 50))

        fill_width = int(bar_width * progress)
        draw.rectangle([bar_x, bar_y, bar_x + fill_width, bar_y + bar_height], fill=(255, 102, 0))

        buffer = BytesIO()
        bg.save(buffer, format="PNG")
        buffer.seek(0)

        return discord.File(fp=buffer, filename="level_card.png")
  
# Setup function
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Level(bot))
