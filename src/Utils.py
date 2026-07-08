from src.Datatypes.Enums import InputMode
from src.Datatypes.Models import Choice, PlayerData, GameMsgType, GameResponse


def get_empty_player_data() -> PlayerData:
    return {
        "name": "",
        "title": "Baron",
        "species": "-",
        "player_class": "-",
        "knowledge": 0,
        "wit": 0,
        "understanding": 0,
        "goal": "",
    }


def make_response(
    text: str,
    input_mode: InputMode = InputMode.NONE,
    choices: list[Choice] | None = None,
    character: PlayerData | None = None,
    title: str = "",
    msg_type: GameMsgType | None = None,
    msg_id: str = "",
    answer_id: str = "",
) -> GameResponse:
    if msg_type is None:
        msg_type = GameMsgType.QUESTION if input_mode is not InputMode.NONE else GameMsgType.INFO

    return {
        "msg_id": msg_id,
        "answer_id": answer_id,
        "msg_type": msg_type,
        "title": title,
        "text": text,
        "input_mode": input_mode,
        "choices": choices or [],
        "character": character or get_empty_player_data(),
    }


def make_choice(choice_id: str, label: str) -> Choice:
    return {"choice_id": choice_id, "label": label}
