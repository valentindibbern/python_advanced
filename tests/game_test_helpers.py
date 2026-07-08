from src.Classes.Game import Game
from src.Datatypes.Models import GameResponse


def choice_ids(response: GameResponse) -> list[str]:
    return [choice["choice_id"] for choice in response["choices"]]


def create_character(
    player_class: str = "class:AUFSTEIGER",
    species: str = "species:HUMAN",
    attribute: str = "attributes:WIT",
) -> tuple[Game, GameResponse]:
    game = Game()
    game.start_game()
    game.handle_text_input(" Testname ")
    game.handle_choice(player_class)
    game.handle_choice(species)
    response = game.handle_choice(attribute)
    return game, response


def enter_ballroom(
    player_class: str = "class:AUFSTEIGER",
    species: str = "species:HUMAN",
    attribute: str = "attributes:WIT",
) -> tuple[Game, GameResponse]:
    game, response = create_character(player_class, species, attribute)
    return game, response


def reach_first_talk(game: Game) -> GameResponse:
    game.handle_choice("continue:look_around")
    game.handle_choice("observe:alena")
    game.handle_choice("observe:bastian")
    game.handle_choice("observe:runa")
    return game.handle_choice("continue:first_talk")


def play_to_council(
    player_class: str,
    species: str,
    attribute: str,
    talk_choice: str,
    royal_choice: str,
    council_choice: str,
) -> tuple[Game, GameResponse]:
    game, _response = enter_ballroom(player_class, species, attribute)
    reach_first_talk(game)
    game.handle_choice(talk_choice)
    game.handle_choice(royal_choice)
    response = game.handle_choice(council_choice)
    return game, response


def play_to_ending(
    player_class: str,
    species: str,
    attribute: str,
    talk_choice: str,
    royal_choice: str,
    council_choice: str,
) -> tuple[Game, GameResponse]:
    game, _response = play_to_council(
        player_class,
        species,
        attribute,
        talk_choice,
        royal_choice,
        council_choice,
    )
    response = game.handle_choice("continue:ending")
    return game, response
