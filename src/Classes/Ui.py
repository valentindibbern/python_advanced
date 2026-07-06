import tkinter as tk
from tkinter import scrolledtext
from typing import TYPE_CHECKING

from src.Enums.InputMode import InputMode

if TYPE_CHECKING:
    from src.Classes.Game import CharacterData, Game, GameResponse
    from src.Classes.Scene import Choice

BACKGROUND = "#050505"
PANEL_BACKGROUND = "#101010"
TEXT_COLOR = "#f2f2f2"
MUTED_TEXT_COLOR = "#b8b8b8"
BORDER_COLOR = "#f2f2f2"
FONT = ("Consolas", 11)
DETAIL_FONT = ("Consolas", 14)


class Ui:
    def __init__(self, game: "Game | None" = None) -> None:
        self.game = game
        self.root = tk.Tk()
        self.root.title("Python Advanced RPG")
        self.root.geometry("1000x700")
        self.root.minsize(700, 450)
        self.root.configure(bg=BACKGROUND)

        self._setup_grid()
        self._create_chat_history()
        self._create_choices_area()
        self._create_character_details()
        self._create_reserved_area()

        if self.game is not None:
            self.show_game_response(self.game.start())

    def _setup_grid(self) -> None:
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=3)
        self.root.rowconfigure(1, weight=1)

    def _create_box(self, row: int, column: int, title: str) -> tk.LabelFrame:
        box = tk.LabelFrame(
            self.root,
            text=title,
            padx=8,
            pady=8,
            bg=PANEL_BACKGROUND,
            fg=TEXT_COLOR,
            bd=1,
            relief="solid",
            highlightbackground=BORDER_COLOR,
            highlightcolor=BORDER_COLOR,
            font=FONT,
        )
        box.grid(row=row, column=column, sticky="nsew", padx=6, pady=6)
        return box

    def _create_chat_history(self) -> None:
        box = self._create_box(0, 0, "History")
        box.rowconfigure(0, weight=1)
        box.columnconfigure(0, weight=1)

        self.chat_history = scrolledtext.ScrolledText(
            box,
            wrap=tk.WORD,
            bg=BACKGROUND,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            selectbackground=TEXT_COLOR,
            selectforeground=BACKGROUND,
            font=FONT,
            relief="flat",
        )
        self.chat_history.grid(row=0, column=0, sticky="nsew")
        self.chat_history.configure(state="disabled")

    def _create_choices_area(self) -> None:
        box = self._create_box(1, 0, "Entscheidungen")
        box.columnconfigure(0, weight=1)
        box.rowconfigure(1, weight=1)

        self.choice_mode_frame = tk.Frame(box, bg=PANEL_BACKGROUND)
        self.choice_mode_frame.grid(row=0, column=0, sticky="nsew")
        self.choice_mode_frame.columnconfigure(0, weight=1)

        self.input_mode_frame = tk.Frame(box, bg=PANEL_BACKGROUND)
        self.input_mode_frame.grid(row=0, column=0, sticky="nsew")
        self.input_mode_frame.columnconfigure(0, weight=1)

        self.empty_choices_frame = tk.Frame(box, bg=PANEL_BACKGROUND)
        self.empty_choices_frame.grid(row=0, column=0, sticky="nsew")

        self._create_choice_mode()
        self._create_input_mode()
        self.show_empty_choices_layout()

    def _create_choice_mode(self) -> None:
        info = tk.Label(
            self.choice_mode_frame,
            text="Wähle eine Option:",
            anchor="w",
            bg=PANEL_BACKGROUND,
            fg=MUTED_TEXT_COLOR,
            font=FONT,
        )
        info.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        self.choice_list_frame = tk.Frame(self.choice_mode_frame, bg=PANEL_BACKGROUND)
        self.choice_list_frame.grid(row=1, column=0, sticky="ew")
        self.choice_list_frame.columnconfigure(0, weight=1)
        self.choice_labels = []

    def _create_input_mode(self) -> None:
        info = tk.Label(
            self.input_mode_frame,
            text="Texteingabe:",
            anchor="w",
            bg=PANEL_BACKGROUND,
            fg=MUTED_TEXT_COLOR,
            font=FONT,
        )
        info.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        self.text_input = tk.Entry(
            self.input_mode_frame,
            bg=BACKGROUND,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            disabledbackground=BACKGROUND,
            disabledforeground=MUTED_TEXT_COLOR,
            relief="solid",
            bd=1,
            font=FONT,
        )
        self.text_input.grid(row=1, column=0, sticky="ew")
        self.text_input.bind("<Return>", self._submit_text_input)

        self.submit_button = tk.Button(
            self.input_mode_frame,
            text="Absenden",
            command=self._submit_text_input,
            bg=BACKGROUND,
            fg=TEXT_COLOR,
            activebackground=TEXT_COLOR,
            activeforeground=BACKGROUND,
            relief="solid",
            bd=1,
            font=FONT,
        )
        self.submit_button.grid(row=2, column=0, sticky="e", pady=(8, 0))

    def show_choice_layout(self) -> None:
        self.choice_mode_frame.tkraise()

    def show_input_layout(self) -> None:
        self.input_mode_frame.tkraise()

    def show_empty_choices_layout(self) -> None:
        self.empty_choices_frame.tkraise()

    def show_game_response(self, response: "GameResponse") -> None:
        self._append_history(response["text"])
        self._update_character_details(response.get("character"))
        self._update_input_area(response)

    def _append_history(self, text: str) -> None:
        self.chat_history.configure(state="normal")
        self.chat_history.insert(tk.END, text + "\n\n")
        self.chat_history.see(tk.END)
        self.chat_history.configure(state="disabled")

    def _update_input_area(self, response: "GameResponse") -> None:
        input_mode = response["input_mode"]

        if response.get("is_finished"):
            self.text_input.configure(state="disabled")
            self.submit_button.configure(state="disabled")
            self.show_empty_choices_layout()
            return

        if input_mode == InputMode.TEXT:
            self.text_input.configure(state="normal")
            self.submit_button.configure(state="normal")
            self.show_input_layout()
            self.text_input.focus_set()
            return

        self.text_input.configure(state="disabled")
        self.submit_button.configure(state="disabled")

        if input_mode == InputMode.CHOICE:
            self._show_choices(response.get("choices", []))
        else:
            self.show_empty_choices_layout()

    def _show_choices(self, choices: list["Choice"]) -> None:
        for label in self.choice_labels:
            label.destroy()

        self.choice_labels = []

        for row, choice in enumerate(choices):
            label = tk.Label(
                self.choice_list_frame,
                text="> " + choice["label"],
                anchor="w",
                bg=BACKGROUND,
                fg=TEXT_COLOR,
                activebackground=TEXT_COLOR,
                activeforeground=BACKGROUND,
                cursor="hand2",
                font=FONT,
                padx=8,
                pady=4,
            )
            label.grid(row=row, column=0, sticky="ew", pady=2)
            label.bind("<Button-1>", lambda event, choice_id=choice["id"]: self._submit_choice(choice_id))
            label.bind("<Enter>", lambda event: event.widget.configure(bg=TEXT_COLOR, fg=BACKGROUND))
            label.bind("<Leave>", lambda event: event.widget.configure(bg=BACKGROUND, fg=TEXT_COLOR))
            self.choice_labels.append(label)

        self.show_choice_layout()

    def _submit_text_input(self, event: object | None = None) -> None:
        if self.game is None:
            return

        text = self.text_input.get()
        self.text_input.delete(0, tk.END)
        response = self.game.handle_text_input(text)
        self.show_game_response(response)

    def _submit_choice(self, choice_id: str) -> None:
        if self.game is None:
            return

        response = self.game.handle_choice(choice_id)
        self.show_game_response(response)

    def _create_character_details(self) -> None:
        box = self._create_box(0, 1, "Charakter")
        box.columnconfigure(0, weight=1)

        self.character_details = tk.Label(
            box,
            text="",
            anchor="nw",
            justify="left",
            bg=PANEL_BACKGROUND,
            fg=TEXT_COLOR,
            font=DETAIL_FONT,
        )
        self.character_details.grid(row=0, column=0, sticky="nsew")
        self._update_character_details(None)

    def _update_character_details(self, character: "CharacterData | None") -> None:
        if character is None:
            details = [
                "Name: -",
                "Spezies: -",
                "Klasse: -",
                "",
                "Attribute",
                "Wissen: -",
                "Schlagfertigkeit: -",
                "Verstaendnis: -",
                "",
                "Ziel: -",
            ]
        else:
            details = [
                f"Name: {character.get('name', '-')}",
                f"Spezies: {character.get('species', '-')}",
                f"Klasse: {character.get('player_class', '-')}",
                "",
                "Attribute",
                f"Wissen: {character.get('knowledge', '-')}",
                f"Schlagfertigkeit: {character.get('wit', '-')}",
                f"Verstaendnis: {character.get('understanding', '-')}",
                "",
                f"Ziel: {character.get('goal', '-')}",
            ]

        self.character_details.configure(text="\n".join(details))

    def _create_reserved_area(self) -> None:
        box = self._create_box(1, 1, "")
        box.columnconfigure(0, weight=1)
        box.rowconfigure(0, weight=1)

        label = tk.Label(
            box,
            text="",
            justify="center",
            bg=PANEL_BACKGROUND,
            fg=MUTED_TEXT_COLOR,
            font=FONT,
        )
        label.grid(row=0, column=0, sticky="nsew")

    def run(self) -> None:
        self.root.mainloop()


def create_ui(game: "Game | None" = None) -> Ui:
    return Ui(game)


if __name__ == "__main__":
    create_ui().run()
