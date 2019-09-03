from enum import Enum
from data_provider import Engine
from data_provider.instagram import InstagramEngine


class EngineType(Enum):
    INSTAGRAM = 1


def get_engine(etype: EngineType) -> Engine:
    if etype is EngineType.INSTAGRAM:
        return InstagramEngine()
    else:
        raise NotImplementedError()
