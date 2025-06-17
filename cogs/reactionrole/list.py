from discord import app_commands
from discord.ext import commands
import discord
class ReactionRoleList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="reactionrole_list", description="List all reaction role panels")
    async def reactionrole_list(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "📋 Current reaction roles:\n1. Role: Gamer, Emoji: 🎮\n2. Role: Artist, Emoji: 🎨",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(ReactionRoleList(bot))
