from typing import TypedDict

from src.Datatypes.Enums import InputMode

class Choice(TypedDict):
    choice_id: str
    label: str

class PlayerData(TypedDict, total=False):
    name: str
    title: str
    species: str
    player_class: str
    knowledge: int
    wit: int
    understanding: int
    goal: str

class GameResponseContent(TypedDict):
    text: str
    input_mode: InputMode
    choices: list[Choice]

class GameResponse(TypedDict):
    id: str
    player_data: PlayerData
    content: GameResponseContent
    is_finished: bool

class UiResponseContent(TypedDict):
    text: str

class UiResponse(TypedDict):
    id: str
    content: UiResponseContent