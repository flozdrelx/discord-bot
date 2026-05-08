import json
from pathlib import Path

def get_data_file(filename: str) -> Path:
    return Path(__file__).resolve().parent.parent / 'data' / filename

def load_config() -> dict:
    config_path = get_data_file('config.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {'roles': {'admin_role_id': [], 'moderator_role_id': []}}

def load_warns() -> dict:
    warns_path = get_data_file('warns.json')
    try:
        with open(warns_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_warns(warns: dict):
    warns_path = get_data_file('warns.json')
    with open(warns_path, 'w') as f:
        json.dump(warns, f, indent=4)

def add_warning(guild_id: str, user_id: str, reason: str):
    warns = load_warns()
    if guild_id not in warns:
        warns[guild_id] = {}
    if user_id not in warns[guild_id]:
        warns[guild_id][user_id] = []
    
    warns[guild_id][user_id].append(reason)
    save_warns(warns)

def get_warnings(guild_id: str, user_id: str) -> list:
    warns = load_warns()
    return warns.get(guild_id, {}).get(user_id, [])

def clear_warning(guild_id: str, user_id: str, warn_id: int) -> bool:
    warns = load_warns()
    user_warns = warns.get(guild_id, {}).get(user_id, [])
    
    if warn_id < 1 or warn_id > len(user_warns):
        return False
        
    del warns[guild_id][user_id][warn_id - 1]
    save_warns(warns)
    return True

def is_higher_or_equal_role(member, interaction_user) -> bool:
    if not hasattr(member, 'top_role') or not hasattr(interaction_user, 'top_role'):
        return False
    return member.top_role.position >= interaction_user.top_role.position
