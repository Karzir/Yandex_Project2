from enum import IntEnum, auto


class Layer(IntEnum):
    BACKGROUND = auto()
    OBSTACLE = auto()
    PLAYER = auto()
    UI = auto()