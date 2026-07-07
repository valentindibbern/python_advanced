from src.Datatypes.Models import Choice, PlayerData, GameResponse, GameResponseContent
from src.Classes.Player import Player

def make_response(
    response_id: str,
    content: GameResponseContent,
    player_data: PlayerData,
    is_finished: bool = False,
) -> GameResponse:
    return {
        "id": response_id,
        "player_data": player_data,
        "content": content,
        "is_finished": is_finished,
    }

def make_choice(choice_id: str, label: str) -> Choice:
    return {"choice_id": choice_id, "label": label}
