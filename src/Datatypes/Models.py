from typing import TypedDict

from Datatypes.Enums import InputMode

class Choice(TypedDict):
    id: str
    label: str

class CharacterData(TypedDict, total=False):
    name: str
    title: str
    species: str
    player_class: str
    knowledge: int
    wit: int
    understanding: int
    goal: str


class GameResponse(TypedDict):
    text: str
    input_mode: InputMode
    choices: list[Choice]
    character: CharacterData | None
    is_finished: bool