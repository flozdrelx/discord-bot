import discord
from discord.ext import commands
from discord import app_commands
from checkrole.is_admin import is_admin, is_admin_slash
from pathlib import Path
from datetime import timedelta
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
from helpers.utils import add_warning, get_warnings, clear_warning, is_higher_or_equal_role

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name='ban')
    @is_admin_slash()
    @app_commands.describe(
        member='The member to ban',
        reason='The reason for the ban'
    )
    async def ban_slash(self, interaction: discord.Interaction, member: discord.Member, reason: str = 'No reason provided.'):
        await member.ban(reason=reason)
        await interaction.response.send_message(f'Banned {member.mention} for {reason}.')

    @commands.command(name='ban')
    @is_admin()
    async def ban_prefix(self, ctx, member: discord.Member, *, reason: str = 'No reason provided.'):
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention} for {reason}.')

    @app_commands.command(name='unban')
    @is_admin_slash()
    @app_commands.describe(
        memberid = 'The member ID to unban'
    )
    async def unban_slash(self, interaction: discord.Interaction, memberid: str):
        try:
            user_id = int(memberid)
        except ValueError:
            await interaction.response.send_message('Please provide a valid numeric user ID.', ephemeral=True)
            return

        try:
            user = await self.bot.fetch_user(user_id)
            await interaction.guild.unban(user)
            await interaction.response.send_message(f'Unbanned {user}.')
        except discord.NotFound:
            await interaction.response.send_message('User not found or not currently banned.', ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message('I do not have permission to unban this user.', ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f'An error occurred: {e}', ephemeral=True)


    @commands.command(name='unban')
    @is_admin()
    async def unban_prefix(self, ctx, memberid: str):
        await ctx.guild.unban(discord.Object(id=int(memberid)))
        await ctx.send(f'Unbanned {memberid}.')

    @app_commands.command(name='lockchannel')
    @is_admin_slash()
    @app_commands.describe(
        channel = 'Channel to lock'
    )
    async def lockchannel_slash(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        await interaction.response.defer()
        
        if channel is None:
            channel = interaction.channel

        default_permissions = channel.overwrites_for(interaction.guild.default_role)

        if default_permissions is None:
            default_permissions = discord.Permissions.none()

        if default_permissions.send_messages == False:
            await interaction.followup.send('Channel is already locked.')
            return

        await channel.set_permissions(interaction.guild.default_role, send_messages=False)
        await interaction.followup.send(f'Locked {channel.mention}.')

    @commands.command(name='lockchannel')
    @is_admin()
    async def lockchannel_prefix(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel

        default_permissions = channel.overwrites_for(ctx.guild.default_role)

        if default_permissions is None:
            default_permissions = discord.Permissions.none()

        if default_permissions.send_messages == False:
            await ctx.send('Channel is already locked.')
            return

        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send(f'Locked {channel.mention}.')

    @app_commands.command(name='unlockchannel')
    @is_admin_slash()
    @app_commands.describe(
        channel = 'Channel to unlock'
    )
    async def unlockchannel_slash(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        await interaction.response.defer()
        
        if channel is None:
            channel = interaction.channel

        default_permissions = channel.overwrites_for(interaction.guild.default_role)

        if default_permissions is None:
            default_permissions = discord.Permissions.none()

        if default_permissions.send_messages == True:
            await interaction.followup.send('Channel is already unlocked.')
            return

        await channel.set_permissions(interaction.guild.default_role, send_messages=True)
        await interaction.followup.send(f'Unlocked {channel.mention}.')

    @commands.command(name='unlockchannel')
    @is_admin()
    async def unlockchannel_prefix(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel

        default_permissions = channel.overwrites_for(ctx.guild.default_role)

        if default_permissions is None:
            default_permissions = discord.Permissions.none()

        if default_permissions.send_messages == True:
            await ctx.send('Channel is already unlocked.')
            return

        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send(f'Unlocked {channel.mention}.')

    @app_commands.command(name='slowmode')
    @is_admin_slash()
    @app_commands.describe(
        channel = 'Channel to set slowmode to',
        time = 'Time to set slowmode to (in seconds)'
    )
    async def slowmode_slash(self, interaction: discord.Interaction, channel: discord.TextChannel = None, time: int = 0):
        await interaction.response.defer()
        
        if channel is None:
            channel = interaction.channel
        
        await channel.edit(slowmode_delay=time)
        await interaction.followup.send(f'Slowmode set to {time} seconds in {channel.mention}.')

    @commands.command(name='slowmode')
    @is_admin()
    async def slowmode_prefix(self, ctx, time: int, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
    
        await channel.edit(slowmode_delay=time)
        await ctx.send(f'Slowmode set to {time} seconds in {channel.mention}.')

    @app_commands.command(name='purge')
    @is_admin_slash()
    @app_commands.describe(
        channel = 'Channel to purge',
        amount = 'Amount of messages to purge'
    )
    async def purge_slash(self, interaction: discord.Interaction, channel: discord.TextChannel = None, amount: int = 0):
        await interaction.response.defer(ephemeral=True)
        
        if channel is None:
            channel = interaction.channel
        
        await channel.purge(limit=amount)
        try:
            await interaction.followup.send(f'Purged {amount} messages in {channel.mention}.')
        except discord.errors.NotFound:
            pass

    @commands.command(name='purge')
    @is_admin()
    async def purge_prefix(self, ctx, amount: int, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
    
        await channel.purge(limit=amount)
        await ctx.send(f'Purged {amount} messages in {channel.mention}.')

    @purge_prefix.error
    async def purge_prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Missing arguments.')

    @purge_slash.error
    async def purge_slash_error(self, interaction: discord.Interaction, error):
        try:
            if interaction.response.is_done():
                await interaction.followup.send(str(error), ephemeral=True)
            else:
                await interaction.response.send_message(str(error), ephemeral=True)
        except discord.errors.NotFound:
            pass

async def setup(bot):
    await bot.add_cog(Admin(bot))