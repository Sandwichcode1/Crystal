import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import json

class OtherReasonModal(discord.ui.Modal, title="Describe Your Issue"):
    reason = discord.ui.TextInput(label="Please describe your issue", style=discord.TextStyle.paragraph, required=True)

    def __init__(self, bot, ctx: discord.interactions):
        self.bot = bot
        self.original_ctx = ctx
        super().__init__()

    async def on_submit(self, ctx: discord.interactions):
        await create_ticket(self.bot, self.original_ctx.user, "Other", self.reason.value, ctx)


async def create_ticket(bot, member, reason_title, reason_detail, ctx):
    guild = ctx.guild

    # Prevent multiple tickets
    for channel in guild.text_channels:
        if channel.topic == f"Ticket for {member.id}":
            await ctx.response.send_message(f"❗ You already have an open ticket: {channel.mention}", ephemeral=True)
            return

    # Set up permissions
    category_name = "🎫 Tickets"
    staff_role_name = "Staff"
    category = discord.utils.get(guild.categories, name=category_name)
    if not category:
        category = await guild.create_category(name=category_name)

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
    }

    staff_role = discord.utils.get(guild.roles, name=staff_role_name)
    if staff_role:
        overwrites[staff_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

    # Create the ticket channel
    channel = await guild.create_text_channel(
        name=f"ticket-{member.name}",
        topic=f"Ticket for {member.id}",
        overwrites=overwrites,
        category=category
    )

    embed = discord.Embed(
        title="🎟️ Ticket Opened",
        description="Thank you for reaching out! A staff member will be with you shortly.",
        color=0x2b2d31
    )
    embed.add_field(name="👤 User", value=member.mention, inline=True)
    embed.add_field(name="📋 Issue", value=f"**{reason_title}**\n{reason_detail}", inline=False)
    embed.set_footer(text=f"User ID: {member.id}")
    embed.timestamp = discord.utils.utcnow()

    await channel.send(embed=embed)
    await ctx.response.send_message(f"✅ Ticket created: {channel.mention}", ephemeral=True)


class ProblemDropdown(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(label="General Question", emoji="❓", description="Ask something"),
            discord.SelectOption(label="Bug Report", emoji="🐛", description="Report a bug or glitch"),
            discord.SelectOption(label="Appeal", emoji="🧾", description="Appeal a punishment"),
            discord.SelectOption(label="Staff Complaint", emoji="🔒", description="Report staff behavior"),
            discord.SelectOption(label="Other", emoji="🛠", description="Something else"),
        ]
        super().__init__(placeholder="What is your problem?", options=options, custom_id="ticket_reason")

    async def callback(self, ctx: discord.interactions):
        choice = self.values[0]
        if choice == "Other":
            modal = OtherReasonModal(self.bot, ctx)
            await ctx.response.send_modal(modal)
        else:
            await create_ticket(self.bot, ctx.user, choice, choice, ctx)


class TicketView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.add_item(ProblemDropdown(bot))


class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    ()
    @app_commands.command(name="ticketmake", description="Send the ticket panel with dropdown")
    async def ticketmake(self, ctx: discord.interactions):
        if not ctx.user.guild_permissions.manage_channels:
            await ctx.response.send_message("You don’t have permission to use this command.", ephemeral=True)
            return

        embed = discord.Embed(
            title="🎫 Create a Ticket",
            description="Select your issue below. A private ticket will be opened and a staff member will assist you shortly.",
            color=0x5865F2
        )
        await ctx.response.send_message(embed=embed, view=TicketView(self.bot))
    ()
    @app_commands.command(name="close", description="Close this ticket")
    async def close(self, ctx: discord.interactions):
        channel = ctx.channel
        if channel.category and channel.name.startswith("ticket-"):
            await ctx.response.send_message("🛑 Closing ticket...", ephemeral=True)
            await asyncio.sleep(1)
            await channel.delete()
        else:
            await ctx.response.send_message("This command can only be used in ticket channels.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Ticket(bot))
    bot.add_view(TicketView(bot))  # Required for persistent dropdown after restart
