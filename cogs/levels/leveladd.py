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
    @app_commands.describe(user="User", amount="Amount of levels")
    async def leveladd(self, interaction: discord.Interaction, user: discord.Member, amount: int):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You need admin permissions.", ephemeral=True)
            return

        with open(self.file_path, "r") as f:
            data = json.load(f)

        uid = str(user.id)
        data.setdefault(uid, {"level": 0})
        data[uid]["level"] += amount

        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

        await interaction.response.send_message(f"✅ Added `{amount}` level(s) to {user.mention}.")

async def setup(bot):
    await bot.add_cog(LevelAdd(bot))
