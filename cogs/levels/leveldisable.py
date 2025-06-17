import json
import discord
from discord.ext import commands
from discord import app_commands

XP_FILE = "xp.json"

class LevelDisable(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _has_staff_permission(self, interaction: discord.Interaction) -> bool:
        return interaction.user.guild_permissions.manage_guild

    @app_commands.command(
        name="leveldisable",
        description="Disable the leveling system in this server."
    )
    async def leveldisable(self, interaction: discord.Interaction):
        if not await self._has_staff_permission(interaction):
            await interaction.response.send_message(
                "❌ You don't have permission to use this command.", ephemeral=True
            )
            return

        guild_id = str(interaction.guild.id)

        try:
            with open(XP_FILE, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        if guild_id not in data:
            data[guild_id] = {"enabled": True, "users": {}}

        data[guild_id]["enabled"] = False

        with open(XP_FILE, "w") as f:
            json.dump(data, f, indent=4)

        await interaction.response.send_message(
            "🚫 Leveling disabled in this server.", ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(LevelDisable(bot))
