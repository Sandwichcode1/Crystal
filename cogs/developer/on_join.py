import discord
from discord.ext import commands

class JoinMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        owner = guild.owner
        if owner is None:
            print(f"Guild {guild.name} has no owner found, skipping join message.")
            return

        embed = discord.Embed(
            title="Setup Instructions for Bot Permissions",
            description=(
                f"Hello {owner.name}, thanks for inviting me to **{guild.name}**!\n\n"
                "To ensure I work properly, please create a role for me that is very high in the role hierarchy.\n"
                "Make sure this role has the following permissions:\n"
                "• Administrator (recommended) or at least Manage Roles, Manage Channels, Send Messages, Embed Links, Read Message History.\n"
                "• Position this role **above all other roles** the bot needs to manage.\n\n"
                "After creating the role, assign it to me to allow me to perform basic and advanced tasks correctly.\n"
                "If you need help, feel free to check my documentation or contact support."
            ),
            color=discord.Color.blue()
        )
        embed.set_footer(text="Crystal Bot • Permission Setup")

        try:
            await owner.send(embed=embed)
            print(f"Sent setup instructions to the owner of {guild.name}")
        except discord.Forbidden:
            print(f"Could not DM the owner of {guild.name} — they might have DMs disabled.")
        except Exception as e:
            print(f"Failed to send setup instructions to owner of {guild.name}: {e}")

async def setup(bot):
    await bot.add_cog(JoinMessage(bot))
