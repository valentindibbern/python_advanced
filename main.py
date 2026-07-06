from src.Classes.Game import Game
from src.Classes.Ui import create_ui


def main() -> None:
    game = Game()
    create_ui(game).run()


if __name__ == "__main__":
    main()
