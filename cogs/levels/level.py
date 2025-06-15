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
        if message.author.bot:
            return

        user_id = str(message.author.id)

        # Load XP data
        with open(XP_FILE, "r") as f:
            data = json.load(f)

        if user_id not in data:
            data[user_id] = {"xp": 0, "level": 0}

        data[user_id]["xp"] += 10

        xp = data[user_id]["xp"]
        level = data[user_id]["level"]
        required = (level + 1) * 100

        if xp >= required:
            data[user_id]["level"] += 1
            data[user_id]["xp"] = 0
            await message.channel.send(f"🎉 {message.author.mention} leveled up to **{level + 1}**!")

        with open(XP_FILE, "w") as f:
            json.dump(data, f)

    @app_commands.command(name="level", description="Check your level.")
    async def level(self, interaction: discord.Interaction):
        user = interaction.user
        user_id = str(user.id)

        # Load XP data
        with open(XP_FILE, "r") as f:
            data = json.load(f)

        if user_id in data:
            xp = data[user_id]["xp"]
            level = data[user_id]["level"]
        else:
            xp = 0
            level = 0

        required = (level + 1) * 100
        progress = xp / required if required > 0 else 0

        image = await self.create_level_card(user, level, xp, required, progress)
        await interaction.response.send_message(file=image)

    async def create_level_card(self, user, level, xp, required, progress):
        card_width = 500
        card_height = 150

        # Load background and resize
        bg = Image.open(BACKGROUND_PATH).convert("RGBA").resize((card_width, card_height))

        # Get user avatar
        asset = user.display_avatar.with_size(128)
        buffer = BytesIO()
        await asset.save(buffer)
        buffer.seek(0)
        pfp = Image.open(buffer).convert("RGBA").resize((64, 64))

        # Paste avatar with transparency mask
        bg.paste(pfp, (20, 20), pfp)

        draw = ImageDraw.Draw(bg)

        # Load fonts
        font_big = ImageFont.truetype(FONT_PATH, 24)
        font_small = ImageFont.truetype(FONT_PATH, 18)

        # Draw user info text
        draw.text((100, 20), str(user.name), font=font_big, fill="white")
        draw.text((100, 50), f"Level: {level}", font=font_small, fill="white")
        draw.text((100, 75), f"XP: {xp}/{required}", font=font_small, fill="white")

        # Draw progress bar background
        bar_x, bar_y = 100, 105
        bar_width, bar_height = 350, 16
        draw.rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + bar_height], fill=(50, 50, 50))

        # Draw progress bar fill
        fill_width = int(bar_width * progress)
        draw.rectangle([bar_x, bar_y, bar_x + fill_width, bar_y + bar_height], fill=(255, 102, 0))

        # Save image to BytesIO buffer
        buffer = BytesIO()
        bg.save(buffer, format="PNG")
        buffer.seek(0)

        return discord.File(fp=buffer, filename="level_card.png")

# *** IMPORTANT: The setup function must be at the bottom, no indentation ***
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Level(bot))
