from discord.ext import commands
from discord import app_commands
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from helpers.utils import load_config

def is_mod():
    async def predicate(ctx):
        config = load_config()
        mod_role_ids = config.get('roles', {}).get('moderator_role_id', [])
        if not isinstance(mod_role_ids, list):
            mod_role_ids = [mod_role_ids]
            
        for role_id in mod_role_ids:
            mod_role = ctx.guild.get_role(role_id)
            if mod_role is not None:
                is_higher_role = (
                    ctx.author.top_role.position >= mod_role.position
                )
                if is_higher_role:
                    return True
                    
        is_owner = ctx.author.id == ctx.guild.owner_id
        return is_owner
    return commands.check(predicate)

def is_mod_slash():
    async def predicate(interaction):
        config = load_config()
        mod_role_ids = config.get('roles', {}).get('moderator_role_id', [])
        if not isinstance(mod_role_ids, list):
            mod_role_ids = [mod_role_ids]
            
        for role_id in mod_role_ids:
            mod_role = interaction.guild.get_role(role_id)
            if mod_role is not None:
                is_higher_role = (
                    interaction.user.top_role.position >= mod_role.position
                )
                if is_higher_role:
                    return True
                    
        is_owner = interaction.user.id == interaction.guild.owner_id
        return is_owner
    return app_commands.check(predicate)