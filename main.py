from src.Classes.Game import Game
from src.Classes.Ui import Ui


def main() -> None:
    game = Game()
    ui = Ui(game)
    ui.run()

if __name__ == "__main__":
    main()
