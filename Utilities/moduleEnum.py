from enum import Enum

class ModuleEnum(Enum):
    CORE = "core"
    MODERATION = "moderation"

    @classmethod
    def list(cls):
        return [m.value for m in cls]