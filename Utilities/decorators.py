def guilds_for():
    """
    Marks a command as guild-bound.
    The actual guild list will be applied dynamically at sync time.
    """
    def wrapper(func):
        setattr(func, "__guild_bound__", True)
        return func
    return wrapper

def module(module_name: str):
    """
    Marks a command as belonging to a specific module.
    Example: @module("core") or @module("moderation")
    """
    def wrapper(func):
        setattr(func, "__module_name__", module_name)
        return func
    return wrapper

