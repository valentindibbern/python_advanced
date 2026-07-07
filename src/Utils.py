from src.Datatypes.Enums import InputMode
from src.Datatypes.Models import Choice, CharacterData, GameResponse

def make_response(
    text: str,
    input_mode: InputMode = InputMode.NONE,
    choices: list[Choice] | None = None,
    character: CharacterData | None = None,
    is_finished: bool = False,
) -> GameResponse:
    return {
        "text": text,
        "input_mode": input_mode,
        "choices": choices or [],
        "character": character,
        "is_finished": is_finished,
    }

def make_choice(id: str, label: str) -> Choice:
    return {"id": id, "label": label}