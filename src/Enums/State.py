from enum import Enum


class State(Enum):
    START = 0
    CHARACTER_CREATION = 1
    WAITING_FOR_TEXT = 2
    WAITING_FOR_CHOICE = 3
    TALKING = 4
    SCENE_COMPLETE = 5
    FINISHED = 6

