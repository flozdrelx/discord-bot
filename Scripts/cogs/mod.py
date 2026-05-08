import discord
from discord.ext import commands
from discord import app_commands
import sys
from pathlib import Path
from datetime import timedelta
from checkrole.is_mod import is_mod, is_mod_slash

sys.path.append(str(Path(__file__).resolve().parent.parent))
from helpers.utils import add_warning, get_warnings, clear_warning, is_higher_or_equal_role

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='kick')
    @is_mod_slash()
    async def kick_slash(self, interaction: discord.Interaction, user: discord.Member, reason: str = 'No reason provided'):
        if user == interaction.user:
            await interaction.response.send_message('You can\'t kick yourself.', ephemeral=True)
            return
        if is_higher_or_equal_role(user, interaction.user):
            await interaction.response.send_message('You can\'t kick someone with a higher or equal role.', ephemeral=True)
            return
        await user.kick(reason=reason)
        await interaction.response.send_message(f'{user.mention} has been kicked by {interaction.user.mention}.')
        await user.send(f'You have been kicked from {interaction.guild.name} by {interaction.user.name}.')

    @commands.command(name='kick')
    @is_mod()
    async def kick_prefix(self, ctx, user: discord.Member, reason: str = 'No reason provided'):
        if user == ctx.author:
            await ctx.send('You can\'t kick yourself.')
            return
        if is_higher_or_equal_role(user, ctx.author):
            await ctx.send('You can\'t kick someone with a higher or equal role.')
            return
        await user.kick(reason=reason)
        await ctx.send(f'{user.mention} has been kicked by {ctx.author.mention}.')
        await user.send(f'You have been kicked from {ctx.guild.name} by {ctx.author.name}.')

    @app_commands.command(name='warn')
    @is_mod_slash()
    async def warn_slash(self, interaction: discord.Interaction, user: discord.Member, reason: str = 'No reason provided'):
        if user == interaction.user:
            await interaction.response.send_message('You can\'t warn yourself.', ephemeral=True)
            return
        if is_higher_or_equal_role(user, interaction.user):
            await interaction.response.send_message('You can\'t warn someone with a higher or equal role.', ephemeral=True)
            return
            
        add_warning(str(interaction.guild.id), str(user.id), reason)
        await user.send(f'You have been warned in {interaction.guild.name} by {interaction.user.name}.')
        await interaction.response.send_message(f'{user.mention} has been warned by {interaction.user.mention}.')

    @commands.command(name='warn')
    @is_mod()
    async def warn_prefix(self, ctx, user: discord.Member, reason: str = 'No reason provided'):
        if user == ctx.author:
            await ctx.send('You can\'t warn yourself.')
            return
        if is_higher_or_equal_role(user, ctx.author):
            await ctx.send('You can\'t warn someone with a higher or equal role.')
            return
            
        add_warning(str(ctx.guild.id), str(user.id), reason)
        await user.send(f'You have been warned in {ctx.guild.name} by {ctx.author.name}.')
        await ctx.send(f'{user.mention} has been warned by {ctx.author.mention}.')

    @app_commands.command(name='warnings')
    @is_mod_slash()
    async def warnings_slash(self, interaction: discord.Interaction, user: discord.Member):
        await interaction.response.defer()
        if user == interaction.user:
            await interaction.followup.send('You can\'t check your own warnings.')
            return
        if is_higher_or_equal_role(user, interaction.user):
            await interaction.followup.send('You can\'t check warnings of someone with a higher or equal role.')
            return
            
        user_warns = get_warnings(str(interaction.guild.id), str(user.id))
        if not user_warns:
            await interaction.followup.send(f'{user.mention} has no warnings.')
            return
            
        await interaction.followup.send(f'{user.mention} has {len(user_warns)} warnings.')

    @commands.command(name='warnings')
    @is_mod()
    async def warnings_prefix(self, ctx, user: discord.Member):
        if user == ctx.author:
            await ctx.send('You can\'t check your own warnings.')
            return
        if is_higher_or_equal_role(user, ctx.author):
            await ctx.send('You can\'t check warnings of someone with a higher or equal role.')
            return
            
        user_warns = get_warnings(str(ctx.guild.id), str(user.id))
        if not user_warns:
            await ctx.send(f'{user.mention} has no warnings.')
            return
            
        await ctx.send(f'{user.mention} has {len(user_warns)} warnings.')

    @app_commands.command(name='clearwarn')
    @is_mod_slash()
    @app_commands.describe(
        member = 'Member to clear a warn',
        warn_id = 'Warn ID to clear'
    )
    async def clearwarn_slash(self, interaction: discord.Interaction, member: discord.Member, warn_id: int):
        await interaction.response.defer()

        if member == interaction.user:
            await interaction.followup.send('You can\'t clear your own warnings.')
            return
        if is_higher_or_equal_role(member, interaction.user):
            await interaction.followup.send('You can\'t clear warnings of someone with a higher or equal role.')
            return
            
        user_warns = get_warnings(str(interaction.guild.id), str(member.id))
        if not user_warns:
            await interaction.followup.send(f'{member.mention} has no warnings.')
            return
            
        success = clear_warning(str(interaction.guild.id), str(member.id), warn_id)
        if not success:
            await interaction.followup.send('Invalid warn ID.')
            return
            
        await interaction.followup.send(f'{member.mention}\'s {warn_id} warn has been cleared.')
    
    @commands.command(name='clearwarn')
    @is_mod()
    async def clearwarn_prefix(self, ctx, member: discord.Member, warn_id: int):
        if member == ctx.author:
            await ctx.send('You can\'t clear your own warnings.')
            return
        if is_higher_or_equal_role(member, ctx.author):
            await ctx.send('You can\'t clear warnings of someone with a higher or equal role.')
            return
            
        user_warns = get_warnings(str(ctx.guild.id), str(member.id))
        if not user_warns:
            await ctx.send(f'{member.mention} has no warnings.')
            return
            
        success = clear_warning(str(ctx.guild.id), str(member.id), warn_id)
        if not success:
            await ctx.send('Invalid warn ID.')
            return
            
        await ctx.send(f'{member.mention}\'s {warn_id} warn has been cleared.')

    @app_commands.command(name='mute')
    @is_mod_slash()
    @app_commands.describe(
        member = 'Member to mute',
        time = 'Time to mute for',
        reason = 'Reason for the mute'
    )
    async def mute_slash(self, interaction: discord.Interaction, member: discord.Member, time: str, reason: str = 'No reason provided.'):
        await interaction.response.defer()

        if member == interaction.user:
            await interaction.followup.send('You can\'t mute yourself.')
            return
        if is_higher_or_equal_role(member, interaction.user):
            await interaction.followup.send('You can\'t mute someone with a higher or equal role.')
            return
        seconds = 0
        if time:
            time_units = {
                'd': 86400,
                'h': 3600,
                'm': 60,
                's': 1
            }
            for unit, seconds_in_unit in time_units.items():
                if time.endswith(unit):
                    try:
                        amount = int(time[:-1])
                        seconds = amount * seconds_in_unit
                        break
                    except ValueError:
                        await interaction.followup.send('Invalid time format.')
                        return
            else:
                await interaction.followup.send('Invalid time format. Use d, h, m, or s (e.g., 1d, 4h, 30m).')
                return
        await member.timeout(timedelta(seconds=seconds), reason=reason)
        await interaction.followup.send(f'{member.mention} has been muted for {time} {reason}.')
    
    @commands.command(name='mute')
    @is_mod()
    async def mute_prefix(self, ctx, member: discord.Member, time: str, reason: str = 'No reason provided.'):
        if member == ctx.author:
            await ctx.send('You can\'t mute yourself.')
            return
        if is_higher_or_equal_role(member, ctx.author):
            await ctx.send('You can\'t mute someone with a higher or equal role.')
            return
        seconds = 0
        if time:
            time_units = {
                'd': 86400,
                'h': 3600,
                'm': 60,
                's': 1
            }
            for unit, seconds_in_unit in time_units.items():
                if time.endswith(unit):
                    try:
                        amount = int(time[:-1])
                        seconds = amount * seconds_in_unit
                        break
                    except ValueError:
                        await ctx.send('Invalid time format.')
                        return
            else:
                await ctx.send('Invalid time format. Use d, h, m, or s (e.g., 1d, 4h, 30m).')
                return
                
        await member.timeout(timedelta(seconds=seconds), reason=reason)
        await ctx.send(f'{member.mention} has been muted for {time} {reason}.')

async def setup(bot):
    await bot.add_cog(Mod(bot))