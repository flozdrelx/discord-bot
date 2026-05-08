from discord.ext import commands
from discord import app_commands
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from helpers.utils import load_config

def is_admin():
    async def predicate(ctx):
        config = load_config()
        admin_role_ids = config.get('roles', {}).get('admin_role_id', [])
        if not isinstance(admin_role_ids, list):
            admin_role_ids = [admin_role_ids]
            
        for role_id in admin_role_ids:
            admin_role = ctx.guild.get_role(role_id)
            if admin_role is not None:
                is_higher_role = (
                    ctx.author.top_role.position >= admin_role.position
                )
                if is_higher_role:
                    return True
                    
        is_owner = ctx.author.id == ctx.guild.owner_id
        return is_owner
    return commands.check(predicate)

def is_admin_slash():
    async def predicate(interaction):
        config = load_config()
        admin_role_ids = config.get('roles', {}).get('admin_role_id', [])
        if not isinstance(admin_role_ids, list):
            admin_role_ids = [admin_role_ids]
            
        for role_id in admin_role_ids:
            admin_role = interaction.guild.get_role(role_id)
            if admin_role is not None:
                is_higher_role = (
                    interaction.user.top_role.position >= admin_role.position
                )
                if is_higher_role:
                    return True
                    
        is_owner = interaction.user.id == interaction.guild.owner_id
        return is_owner
    return app_commands.check(predicate)