import discord
from discord.ext import commands
from discord import app_commands

class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="invite", description="Show invite markdown text")
    async def invite(self, interaction: discord.Interaction):
        # Corrected markdown link with closing parenthesis
        markdown_link = "[Add me to your server](https://discord.com/oauth2/authorize?client_id=1383061358957957120&permissions=1719631854169335&integration_type=0&scope=applications.commands+bot)"

        # This shows clickable text inside a normal message, not a code block
        await interaction.response.send_message(markdown_link, ephemeral=False)

async def setup(bot):
    await bot.add_cog(Invite(bot))
