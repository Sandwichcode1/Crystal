from discord import app_commands
from discord.ext import commands
import discord
class ReactionRoleDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="reactionrole_delete", description="Delete a reaction role panel")
    async def reactionrole_delete(self, interaction: discord.Interaction):
        await interaction.response.send_message("🗑️ Reaction role panel deleted.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ReactionRoleDelete(bot))
