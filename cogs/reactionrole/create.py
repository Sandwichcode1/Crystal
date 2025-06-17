from discord import app_commands, ui
from discord.ext import commands
import discord

class ReactionRoleModal(ui.Modal, title="Create Reaction Role"):
    role_name = ui.TextInput(label="Role Name", placeholder="e.g. Gamer", required=True)
    emoji = ui.TextInput(label="Emoji", placeholder="e.g. 🎮", required=True)

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"✅ Reaction Role created: Role: **{self.role_name.value}**, Emoji: {self.emoji.value}",
            ephemeral=True
        )

class ReactionRoleCreate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="reactionrole_create", description="Create a reaction role panel")
    async def reactionrole_create(self, interaction: discord.Interaction):
        await interaction.response.send_modal(ReactionRoleModal(self.bot))

async def setup(bot):
    await bot.add_cog(ReactionRoleCreate(bot))
