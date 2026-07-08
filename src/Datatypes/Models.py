from enum import Enum
from typing import TypedDict

from src.Datatypes.Enums import Attributes, InputMode


class GameMsgType(Enum):
    INFO = "info"
    QUESTION = "question"
    ERROR = "error"
    END = "end"


class UiMsgType(Enum):
    START = "start"
    TEXT = "text"
    CHOICE = "choice"


class Choice(TypedDict):
    choice_id: str
    label: str


class AttributeCheck(TypedDict):
    attribute: Attributes
    attribute_label: str
    difficulty: int
    roll: int
    attribute_value: int
    total: int
    success: bool


class PlayerData(TypedDict):
    name: str
    title: str
    species: str
    player_class: str
    knowledge: int
    wit: int
    understanding: int
    goal: str
    goal_status: str


class GameResponse(TypedDict):
    msg_id: str
    answer_id: str
    msg_type: GameMsgType
    title: str
    text: str
    input_mode: InputMode
    choices: list[Choice]
    character: PlayerData

class UiResponse(TypedDict):
    msg_id: str
    msg_type: UiMsgType
    content: str
    choice_id: str
