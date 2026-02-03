from typing import List
from discord import app_commands

REGISTERED_GROUPS: List[app_commands.Group] = []

def create_group(name: str, description: str) -> app_commands.Group:
    """
    Create a Group that is NOT auto-registered anywhere.

    We only store it in REGISTERED_GROUPS so the sync engine
    can decide when and where to register it per guild.
    """
    group = app_commands.Group(name=name, description=description)
    REGISTERED_GROUPS.append(group)
    return group
