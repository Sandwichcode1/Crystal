import os
import discord
from discord.ext import commands, tasks
from fastapi import FastAPI
import uvicorn
import asyncio

app = FastAPI()

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cog_folders = [
    "fun_and_more", "levels", "moderation", "roles",
    "automod", "developer", "reactionrole", "giveaway"
]

async def load_cogs():
    for folder in cog_folders:
        folder_path = os.path.join(BASE_DIR, "cogs", folder)
        if not os.path.exists(folder_path):
            print(f"Folder not found: {folder_path}")
            continue
        for filename in os.listdir(folder_path):
            if filename.endswith(".py"):
                cog_path = f"cogs.{folder}.{filename[:-3]}"
                try:
                    await bot.load_extension(cog_path)
                    print(f"🔧 Loaded cog: {cog_path}")
                except Exception as e:
                    print(f"❌ Failed to load cog {cog_path}: {e}")

@tasks.loop(minutes=10)
async def update_status():
    server_count = len(bot.guilds)
    member_count = sum(g.member_count for g in bot.guilds if g.member_count)
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name=f"{server_count} servers & {member_count} members"
    ))

@app.get("/")
async def home():
    return {"status": "Bot is alive!"}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("----------------------------------------------")

    try:
        synced = await bot.tree.sync()
        print(f"✅ Slash commands synced globally! Total synced commands: {len(synced)}")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

    print("\nAll loaded cogs and their commands:")
    for cog_name, cog_obj in bot.cogs.items():
        cmds = [cmd.name for cmd in cog_obj.get_commands()]
        print(f"- {cog_name}: {cmds}")

    update_status.start()

async def main():
    await load_cogs()
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("ERROR: DISCORD_TOKEN not set in environment variables!")
        return

    bot_task = asyncio.create_task(bot.start(token))
    api_task = asyncio.create_task(
        uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
    )

    await asyncio.gather(bot_task, api_task)

if __name__ == "__main__":
    asyncio.run(main())
