import discord
from discord.ext import commands
import json
import os
from discord import app_commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_file = "welcome_config.json"
        if not os.path.exists(self.config_file):
            with open(self.config_file, "w") as f:
                json.dump({}, f)

    def _load_config(self):
        with open(self.config_file, "r") as f:
            return json.load(f)

    def _save_config(self, config):
        with open(self.config_file, "w") as f:
            json.dump(config, f, indent=4)

    # Convert this to a slash command properly
    @app_commands.command(name="setwelcomechannel", description="Set the welcome channel")
    async def setwelcomechannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        config = self._load_config()
        config[str(interaction.guild.id)] = channel.id
        self._save_config(config)
        await interaction.response.send_message(f"✅ Welcome channel set to {channel.mention}", ephemeral=True)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        config = self._load_config()
        channel_id = config.get(str(member.guild.id))
        if not channel_id:
            return  # No welcome channel set for this guild

        channel = member.guild.get_channel(channel_id)
        if not channel:
            return  # Channel not found

        embed = discord.Embed(
            title=f"Welcome to {member.guild.name}, {member.name}!",
            description=f"👋 Hey {member.mention}, welcome to **{member.guild.name}**! Enjoy your stay!",
            color=discord.Color.blurple()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        
        embed.set_footer(text="Welcome to the server!")
        embed.timestamp = discord.utils.utcnow()

        await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Welcome(bot))
