import discord
from discord.ext import commands
from discord import app_commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='help')
    async def help_slash(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title='Bot Commands',
            description='List of all available commands.',
            color=discord.Color.blue()
        )

        embed.add_field(
            name='General Commands',
            value=
            '`/userinfo [member]` or `!userinfo [member]`\n'
            'Shows information about a member.\n\n'

            '`/serverinfo` or `!serverinfo`\n'
            'Shows information about the server.\n\n'

            '`/avatar [member]` or `!avatar [member]`\n'
            'Shows a member avatar.\n\n'

            '`/say <text>` or `!say <text>`\n'
            'Makes the bot say something.\n\n'

            '`/fakeban [member] [reason]` or `!fakeban [member] [reason]`\n'
            'Fake bans a member for fun.',
            inline=False
        )

        embed.add_field(
            name='Moderator Commands',
            value=
            '`/kick <member> [reason]` or `!kick <member> [reason]`\n'
            'Kicks a member.\n\n'

            '`/warn <member> [reason]` or `!warn <member> [reason]`\n'
            'Warns a member.\n\n'

            '`/warnings <member>` or `!warnings <member>`\n'
            'Shows warnings of a member.\n\n'

            '`/clearwarn <member> <warn_id>` or `!clearwarn <member> <warn_id>`\n'
            'Clears a warning.\n\n'

            '`/mute <member> <time> [reason]` or `!mute <member> <time> [reason]`\n'
            'Mutes a member.\n'
            'Example: `1d`, `4h`, `30m`, `10s`',
            inline=False
        )

        embed.add_field(
            name='Admin Commands',
            value=
            '`/ban <member> [reason]` or `!ban <member> [reason]`\n'
            'Bans a member.\n\n'

            '`/unban <userid>` or `!unban <userid>`\n'
            'Unbans a user.\n\n'

            '`/lockchannel [channel]` or `!lockchannel [channel]`\n'
            'Locks a channel.\n\n'

            '`/unlockchannel [channel]` or `!unlockchannel [channel]`\n'
            'Unlocks a channel.\n\n'

            '`/slowmode [channel] <seconds>` or `!slowmode <seconds> [channel]`\n'
            'Sets channel slowmode.\n\n'

            '`/purge <amount> [channel]` or `!purge <amount> [channel]`\n'
            'Deletes messages.',
            inline=False
        )

        embed.set_footer(text='Use slash commands or prefix commands.')

        await interaction.response.send_message(embed=embed)

    @commands.command(name='help')
    async def help_prefix(self, ctx):
        embed = discord.Embed(
            title='Bot Commands',
            description='List of all available commands.',
            color=discord.Color.blue()
        )

        embed.add_field(
            name='General Commands',
            value=
            '`!userinfo [member]`\n'
            '`!serverinfo`\n'
            '`!avatar [member]`\n'
            '`!say <text>`\n'
            '`!fakeban [member] [reason]`',
            inline=False
        )

        embed.add_field(
            name='Moderator Commands',
            value=
            '`!kick <member> [reason]`\n'
            '`!warn <member> [reason]`\n'
            '`!warnings <member>`\n'
            '`!clearwarn <member> <warn_id>`\n'
            '`!mute <member> <time> [reason]`',
            inline=False
        )

        embed.add_field(
            name='Admin Commands',
            value=
            '`!ban <member> [reason]`\n'
            '`!unban <userid>`\n'
            '`!lockchannel [channel]`\n'
            '`!unlockchannel [channel]`\n'
            '`!slowmode <seconds> [channel]`\n'
            '`!purge <amount> [channel]`',
            inline=False
        )

        embed.set_footer(text='You can also use slash commands.')

        await ctx.send(embed=embed)

    @app_commands.command(name='userinfo')
    @app_commands.describe(
        member = 'Member to get information about'
    )
    async def userinfo_slash(self, interaction: discord.Interaction, member: discord.Member = None):
        await interaction.response.defer()

        if member is None:
            member = interaction.user
        embed = discord.Embed(
            title=f'{member.name}\'s Information',
            color=discord.Color.blue()
        )
        embed.add_field(name='ID', value=member.id, inline=True)
        embed.add_field(name='Name', value=member.name, inline=True)
        embed.add_field(name='Nickname', value=member.nick, inline=True)
        embed.add_field(name='Top Role', value=member.top_role, inline=True)
        embed.add_field(name='Created At', value=member.created_at, inline=True)
        embed.add_field(name='Joined At', value=member.joined_at, inline=True)
        embed.set_thumbnail(url=member.display_avatar.url)
        await interaction.followup.send(embed=embed)

    

    @commands.command(name='userinfo')
    async def userinfo_prefix(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(
            title=f'{member.name}\'s Information',
            color=discord.Color.blue()
        )
        embed.add_field(name='ID', value=member.id, inline=True)
        embed.add_field(name='Name', value=member.name, inline=True)
        embed.add_field(name='Nickname', value=member.nick, inline=True)
        embed.add_field(name='Top Role', value=member.top_role, inline=True)
        embed.add_field(name='Created At', value=member.created_at, inline=True)
        embed.add_field(name='Joined At', value=member.joined_at, inline=True)
        embed.set_thumbnail(url=member.display_avatar.url)
        await ctx.send(embed=embed)

    @app_commands.command(name='serverinfo')
    async def serverinfo_slash(self, interaction: discord.Interaction):
        await interaction.response.defer()

        guild = interaction.guild

        embed = discord.Embed(
            title=f'{guild.name}\'s Information',
            color=discord.Color.blue()
        )
        embed.add_field(name='ID', value=guild.id, inline=True)
        embed.add_field(name='Name', value=guild.name, inline=True)
        embed.add_field(name='Owner', value=guild.owner, inline=True)
        embed.add_field(name='Member Count', value=guild.member_count, inline=True)
        embed.add_field(name='Created At', value=guild.created_at, inline=True)
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        await interaction.followup.send(embed=embed)

    @commands.command(name='serverinfo')
    async def serverinfo_prefix(self, ctx, guild: discord.Guild = None):
        if guild is None:
            guild = ctx.guild

        embed = discord.Embed(
            title=f'{guild.name}\'s Information',
            color=discord.Color.blue()
        )
        embed.add_field(name='ID', value=guild.id, inline=True)
        embed.add_field(name='Name', value=guild.name, inline=True)
        embed.add_field(name='Owner', value=guild.owner, inline=True)
        embed.add_field(name='Member Count', value=guild.member_count, inline=True)
        embed.add_field(name='Created At', value=guild.created_at, inline=True)
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        await ctx.send(embed=embed)

    @app_commands.command(name='avatar')
    @app_commands.describe(
        member = 'Member to get avatar of'
    )
    async def avatar_slash(self, interaction: discord.Interaction, member: discord.Member = None):
        await interaction.response.defer()

        if member is None:
            member = interaction.user
        embed = discord.Embed(
            title=f'{member.name}\'s Avatar',
            color=discord.Color.blue()
        )
        embed.set_image(url=member.display_avatar.url)
        await interaction.followup.send(embed=embed)

    @commands.command(name='avatar')
    async def avatar_prefix(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(
            title=f'{member.name}\'s Avatar',
            color=discord.Color.blue()
        )
        embed.set_image(url=member.display_avatar.url)
        await ctx.send(embed=embed)

    @app_commands.command(name='say')
    @app_commands.describe(
        text = 'Text to say'
    )
    async def say_slash(self, interaction: discord.Interaction, text: str):
        await interaction.response.send_message("Message sent", ephemeral=True)
        await interaction.channel.send(text)

    @commands.command(name='say')
    async def say_prefix(self, ctx, *, text: str):
        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            pass
        await ctx.send(text)

    @app_commands.command(name='fakeban')
    @app_commands.describe(
        member = 'Member to fake ban',
        reason = 'Reason for the fake ban'
    )
    async def fakeban_slash(self, interaction: discord.Interaction, member: discord.Member = None, reason: str = 'No reason provided'):
        await interaction.response.send_message("Fake ban sent", ephemeral=True)

        if member is None:
            member = interaction.user
        embed = discord.Embed(
            title=f'{member.name} has been banned',
            description=f'**Reason:** {reason}',
            color=discord.Color.red()
        )
        await interaction.channel.send(embed=embed)

    @commands.command(name='fakeban')
    async def fakeban_prefix(self, ctx, member: discord.Member = None, *, reason: str = 'No reason provided'):
        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            pass
            
        if member is None:
            member = ctx.author
        embed = discord.Embed(
            title=f'{member.name} has been banned',
            description=f'**Reason:** {reason}',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))