import discord
from discord.ext import commands
from discord import app_commands
import json
import os

SUGGESTION_FILE = "suggestions.json"

class SuggestionList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not os.path.exists(SUGGESTION_FILE):
            with open(SUGGESTION_FILE, "w") as f:
                json.dump({}, f)

    def load_suggestions(self):
        with open(SUGGESTION_FILE, "r") as f:
            return json.load(f)

    @app_commands.command(name="suggestionlist", description="Show all suggestions for this server")
    async def suggestionlist(self, interaction: discord.Interaction):
        data = self.load_suggestions()
        guild_id = str(interaction.guild.id)

        if guild_id not in data or not data[guild_id]:
            await interaction.response.send_message("❌ No suggestions found for this server.", ephemeral=True)
            return

        embed = discord.Embed(title="📋 Suggestions", color=discord.Color.blue())
        
        for idx, suggestion in enumerate(data[guild_id], 1):
            user = suggestion.get("user", "Unknown user")
            text = suggestion.get("suggestion", "No suggestion text")
            embed.add_field(name=f"#{idx} by {user}", value=text, inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(SuggestionList(bot))
