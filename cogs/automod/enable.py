import json
import os
from discord.ext import commands
from discord import app_commands
import discord

class AutomodEnable(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.status_file = "automod_status.json"
        if not os.path.exists(self.status_file):
            with open(self.status_file, "w") as f:
                json.dump({}, f)

    def _load_status(self):
        with open(self.status_file, "r") as f:
            return json.load(f)

    def _save_status(self, data):
        with open(self.status_file, "w") as f:
            json.dump(data, f, indent=4)

    async def has_staff_permission(self, interaction: discord.Interaction) -> bool:
        return interaction.user.guild_permissions.manage_guild

    @app_commands.command(name="automod_enable", description="Enable AutoMod for this server")
    async def automod_enable(self, interaction: discord.Interaction):
        if not await self.has_staff_permission(interaction):
            await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
            return

        data = self._load_status()
        guild_id = str(interaction.guild_id)

        if data.get(guild_id, {}).get("enabled") is True:
            msg = "⚠️ AutoMod is already enabled."
        else:
            data[guild_id] = {"enabled": True}
            self._save_status(data)
            msg = "✅ AutoMod has been enabled for this server."

        await interaction.response.send_message(msg, ephemeral=True)

async def setup(bot):
    await bot.add_cog(AutomodEnable(bot))
