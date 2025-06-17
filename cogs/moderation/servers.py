import discord
from discord import app_commands
from discord.ext import commands

class ServerList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="servers", description="List all servers the bot is in")
    async def servers(self, interaction: discord.Interaction):
        if interaction.user.id != 976469246936756246:  # Replace with your Discord ID
            await interaction.response.send_message("❌ You aren't authorized to use this command.", ephemeral=True)
            return

        server_lines = []

        for guild in self.bot.guilds:
            invite_link = "*No invite (no permission)*"
            try:
                for channel in guild.text_channels:
                    if channel.permissions_for(guild.me).create_instant_invite:
                        invite = await channel.create_invite(max_age=0, max_uses=0, unique=False)
                        invite_link = f"[Invite Link]({invite.url})"
                        break
            except Exception:
                invite_link = "*Error creating invite*"

            server_lines.append(
                f"• **{guild.name}** (`{guild.id}`) – {guild.member_count} members\n→ {invite_link}"
            )

        description = "\n\n".join(server_lines) or "The bot is not in any servers."

        embed = discord.Embed(
            title=f"🤖 Connected Servers ({len(self.bot.guilds)})",
            description=description[:4096],  # Discord embed description limit
            color=discord.Color.green()
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(ServerList(bot))
