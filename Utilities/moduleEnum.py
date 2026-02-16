from enum import Enum

class ModuleEnum(Enum):
    CORE = "core"
    MODERATION = "moderation"
    FUN = "fun"
    LOGGING = "logging"

    @classmethod
    def list(cls):
        return [m.value for m in cls]