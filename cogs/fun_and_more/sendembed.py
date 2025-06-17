import discord
from discord.ext import commands
from discord import app_commands

class EmbedCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="sendembed", description="Send a custom embed")
    @app_commands.describe(
        text="Main text in the embed",
        title="Optional title for the embed",
        footer="Optional footer text",
        color="Optional HEX color (default is pale yellow: #fff9b0)"
    )
    async def sendembed(
        self,
        interaction: discord.Interaction,
        text: str,
        title: str = None,
        footer: str = None,
        color: str = "#fff9b0"
    ):
        # Admin-only check
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You must be an admin to use this command.", ephemeral=True)
            return

        # Convert HEX color string to discord.Color
        try:
            embed_color = discord.Color(int(color.strip("#"), 16))
        except ValueError:
            await interaction.response.send_message("❌ Invalid HEX color format.", ephemeral=True)
            return

        embed = discord.Embed(description=text, color=embed_color)
        if title:
            embed.title = title
        if footer:
            embed.set_footer(text=footer)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(EmbedCommands(bot))
