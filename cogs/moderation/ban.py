from discord import app_commands
from discord.ext import commands
import discord

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ban", description="Ban a user")
    @app_commands.describe(user="User to ban", reason="Reason for ban")
    async def ban(self, interaction: discord.Interaction, user: discord.Member, reason: str = None):
        try:
            await user.ban(reason=reason)
            await interaction.response.send_message(f"{user} has been banned.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I do not have permission to ban that user.", ephemeral=True)
        except discord.HTTPException:
            await interaction.response.send_message("Banning failed. Please try again later.", ephemeral=True)

    @app_commands.command(name="unban", description="Unban a user by their username#discriminator")
    @app_commands.describe(user="The username#discriminator of the user to unban (e.g. SomeUser#1234)")
    async def unban(self, interaction: discord.Interaction, user: str):
        guild = interaction.guild
        banned_users = await guild.bans()
        user_name, user_discriminator = user.split('#')

        for ban_entry in banned_users:
            banned_user = ban_entry.user
            if (banned_user.name, banned_user.discriminator) == (user_name, user_discriminator):
                try:
                    await guild.unban(banned_user)
                    await interaction.response.send_message(f"Unbanned {banned_user}.", ephemeral=True)
                except discord.Forbidden:
                    await interaction.response.send_message("I do not have permission to unban that user.", ephemeral=True)
                except discord.HTTPException:
                    await interaction.response.send_message("Unbanning failed. Please try again later.", ephemeral=True)
                return
        
        await interaction.response.send_message(f"User {user} not found in ban list.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
