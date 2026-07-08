import tkinter as tk
from tkinter import scrolledtext

from src.Datatypes.Enums import InputMode
from src.Classes.Game import Game
from src.Datatypes.Models import Choice, GameMsgType, GameResponse, PlayerData, UiMsgType, UiResponse

BACKGROUND = "#050505"
PANEL_BACKGROUND = "#101010"
TEXT_COLOR = "#f2f2f2"
MUTED_TEXT_COLOR = "#b8b8b8"
BORDER_COLOR = "#f2f2f2"
FONT = ("Consolas", 11)
DETAIL_FONT = ("Consolas", 14)


def _disable_all(*widgets: tk.Button | tk.Entry) -> None:
    for widget in widgets:
        widget.configure(state="disabled")

def _normalize_all(*widgets: tk.Button | tk.Entry) -> None:
    for widget in widgets:
        widget.configure(state="normal")


class Ui:
    def __init__(self, game: Game) -> None:
        self.game = game
        self.message_count: int = 0
        self.root = tk.Tk()
        self.root.title("Python Advanced RPG")
        self.root.geometry("1000x700")
        self.root.minsize(700, 450)
        self.root.configure(bg=BACKGROUND)

        self._setup_grid()
        self._create_chat_history()
        self._create_choices_area()
        self._create_character_details(self.game.player.get_character_data())
        self._create_control_area()
        self.accept(self.game.start())

    def _append_history(self, text: str) -> None:
        self.chat_history.configure(state="normal")
        self.chat_history.insert(tk.END, text + "\n\n")
        self.chat_history.see(tk.END)
        self.chat_history.configure(state="disabled")

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

    def _create_character_details(self, player_data: PlayerData) -> None:
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
        self._update_character_details(player_data)

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
        # Es muss ein lamda dazwischen stehen damit event abgefangen wird.
        self.text_input.bind("<Return>", lambda event: self._submit_text_input())

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

    def _create_control_area(self) -> None:
        box = self._create_box(1, 1, "Spiel")
        box.columnconfigure(0, weight=1)
        box.rowconfigure(2, weight=1)

        self.start_button: tk.Button = tk.Button(
            box,
            text="Start",
            command=self._start_game,
            bg=BACKGROUND,
            fg=TEXT_COLOR,
            activebackground=TEXT_COLOR,
            activeforeground=BACKGROUND,
            relief="solid",
            bd=1,
            font=FONT,
        )
        self.start_button.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        self.stop_button: tk.Button = tk.Button(
            box,
            text="Stop",
            command=self._stop_game,
            bg=PANEL_BACKGROUND,
            fg=TEXT_COLOR,
            activebackground=TEXT_COLOR,
            activeforeground=BACKGROUND,
            relief="solid",
            bd=1,
            font=FONT,
        )
        self.stop_button.grid(row=1, column=0, sticky="ew")

    def _setup_grid(self) -> None:
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=3)
        self.root.rowconfigure(1, weight=1)

    def _show_choices(self, choices: list[Choice]) -> None:
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
            label.bind("<Button-1>", lambda event, choice_id=choice["choice_id"]: self._submit_choice(choice_id))
            label.bind("<Enter>", lambda event: event.widget.configure(bg=TEXT_COLOR, fg=BACKGROUND))
            label.bind("<Leave>", lambda event: event.widget.configure(bg=BACKGROUND, fg=TEXT_COLOR))
            self.choice_labels.append(label)

        self.show_choice_layout()

    def _submit_text_input(self) -> None:
        text = self.text_input.get()
        self.text_input.delete(0, tk.END)
        ui_response: UiResponse = self._make_ui_response(UiMsgType.TEXT, content=text)
        response = self.game.handle_ui_response(ui_response)
        self.accept(response)

    def _submit_choice(self, choice_id: str) -> None:
        ui_response: UiResponse = self._make_ui_response(UiMsgType.CHOICE, choice_id=choice_id)
        response = self.game.handle_ui_response(ui_response)
        self.accept(response)

    def _start_game(self) -> None:
        response = self.game.start_game()
        self.start_button.configure(state="disabled")
        self.accept(response)

    def _stop_game(self) -> None:
        self.root.destroy()

    def _make_ui_response(self, msg_type: UiMsgType, content: str = "", choice_id: str = "") -> UiResponse:
        self.message_count += 1
        return {
            "msg_id": f"ui-{self.message_count}-{msg_type.value}",
            "msg_type": msg_type,
            "content": content,
            "choice_id": choice_id,
        }

    def _update_input_area(self, response: GameResponse) -> None:
        if response["msg_type"] == GameMsgType.END:
            _disable_all(self.text_input, self.submit_button)
            self.show_empty_choices_layout()
            return

        if response["input_mode"] == InputMode.TEXT:
            _normalize_all(self.text_input, self.submit_button)
            self.show_input_layout()
            self.text_input.focus_set()
            return

        _disable_all(self.text_input, self.submit_button)

        if response["input_mode"] == InputMode.CHOICE:
            self._show_choices(response["choices"])
        else:
            self.show_empty_choices_layout()

    def _update_character_details(self, player_data: PlayerData) -> None:
        details = [
            f"Name: {player_data['name'] if player_data['name'] else ' - '}",
            f"Titel: {player_data['title']}",
            f"Spezies: {player_data['species'] if player_data['species'] else ' - '}",
            f"Klasse: {player_data['player_class'] if player_data['player_class'] else ' - '}",
            "",
            "Attribute",
            f"Wissen: {player_data['knowledge']}",
            f"Schlagfertigkeit: {player_data['wit']}",
            f"Verständnis: {player_data['understanding']}",
            "",
            f"Ziel: {player_data['goal'] if player_data['goal'] else ' - '}",
            f"Status: {player_data['goal_status'] if player_data['goal_status'] else ' - '}",
        ]

        self.character_details.configure(text="\n".join(details))

    def show_choice_layout(self) -> None:
        self.choice_mode_frame.tkraise()

    def show_input_layout(self) -> None:
        self.input_mode_frame.tkraise()

    def show_empty_choices_layout(self) -> None:
        self.empty_choices_frame.tkraise()

    def accept(self, response: GameResponse) -> None:
        if response["title"]:
            self._append_history(response["title"] + "\n\n" + response["text"])
        else:
            self._append_history(response["text"])
        self._update_character_details(response["character"])
        self._update_input_area(response)

    def run(self) -> None:
        self.root.mainloop()
