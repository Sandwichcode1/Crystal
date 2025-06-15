import discord
from discord.ext import commands
import os
import threading
from flask import Flask

# --- Web Server Setup (to keep alive) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    thread = threading.Thread(target=run)
    thread.start()

# --- Discord Bot Setup ---
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cog_folders = ["fun_and_more", "levels", "moderation", "roles"]
GUILD_ID = 1383064822350090421  # replace with your test server ID as int

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    await bot.tree.sync()
    guild = discord.Object(id=GUILD_ID)
    synced_commands = await bot.tree.sync(guild=guild)
    print(f"Slash commands synced! Total synced commands: {len(bot.tree.get_commands())}")

async def load_cogs():
    for folder in cog_folders:
        folder_path = os.path.join(BASE_DIR, "cogs", folder)
        for filename in os.listdir(folder_path):
            if filename.endswith(".py"):
                cog_path = f"cogs.{folder}.{filename[:-3]}"
                try:
                    await bot.load_extension(cog_path)
                    print(f"🔧 Loaded cog: {cog_path}")
                except Exception as e:
                    print(f"Failed to load cog {cog_path}: {e}")

@bot.event
async def on_connect():
    await load_cogs()

# --- Keep alive ---
keep_alive()

# --- Run the bot ---
bot.run("MTM4MzA2MTM1ODk1Nzk1NzEyMA.GF3eZF.hejnv-tdzoQbaQqE4_IJAwnjOhkxJzoI7MS2mM")
