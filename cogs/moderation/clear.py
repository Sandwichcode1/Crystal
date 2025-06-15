import discord
from discord.ext import commands
from discord import app_commands

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clear", description="Delete a number of messages.")
    @app_commands.describe(amount="Number of messages to delete.")
    async def clear(self, interaction: discord.Interaction, amount: int):
        # Defer the interaction to avoid timeout
        await interaction.response.defer(ephemeral=True)

        # Delete the messages
        deleted = await interaction.channel.purge(limit=amount)

        # Follow up with the response
        await interaction.followup.send(f"🧹 Deleted {len(deleted)} messages.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Clear(bot))
