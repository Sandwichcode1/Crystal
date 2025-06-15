import discord
from discord.ext import commands
from discord import app_commands

class Warn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warnings = {}

    @app_commands.command(name="warn", description="Warn a user.")
    @app_commands.describe(member="The member to warn", reason="Reason for warning")
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        if member.id not in self.warnings:
            self.warnings[member.id] = []
        self.warnings[member.id].append(reason)
        await interaction.response.send_message(f"⚠️ Warned {member.mention} for: {reason}")

async def setup(bot):
    await bot.add_cog(Warn(bot))
