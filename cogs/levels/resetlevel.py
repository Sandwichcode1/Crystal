import discord, json, os
from discord.ext import commands
from discord import app_commands

class ResetLevel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file_path = "cogs/level_data.json"
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump({}, f)

    @app_commands.command(name="resetlevel", description="Reset a user's level")
    @app_commands.describe(user="User to reset")
    async def resetlevel(self, interaction: discord.Interaction, user: discord.Member):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You need admin permissions.", ephemeral=True)
            return

        with open(self.file_path, "r") as f:
            data = json.load(f)

        uid = str(user.id)
        if uid in data:
            data[uid]["level"] = 0
        else:
            data[uid] = {"level": 0}

        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

        await interaction.response.send_message(f"🧹 Reset level for {user.mention}.")

async def setup(bot):
    await bot.add_cog(ResetLevel(bot))
