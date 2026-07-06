import tkinter as tk
from tkinter import scrolledtext


BACKGROUND = "#050505"
PANEL_BACKGROUND = "#101010"
TEXT_COLOR = "#f2f2f2"
MUTED_TEXT_COLOR = "#b8b8b8"
BORDER_COLOR = "#f2f2f2"
FONT = ("Consolas", 11)
DETAIL_FONT = ("Consolas", 14)


class Ui:
    def __init__(self, game=None):
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

    def _setup_grid(self):
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=3)
        self.root.rowconfigure(1, weight=1)

    def _create_box(self, row, column, title):
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

    def _create_chat_history(self):
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

    def _create_choices_area(self):
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

    def _create_choice_mode(self):
        info = tk.Label(
            self.choice_mode_frame,
            text="Wähle eine Option:",
            anchor="w",
            bg=PANEL_BACKGROUND,
            fg=MUTED_TEXT_COLOR,
            font=FONT,
        )
        info.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        self.choice_labels = []
        options = (
            "> Mit dem Baron sprechen",
            "> Den Saal beobachten",
            "> Zum Archiv gehen",
        )
        for row, text in enumerate(options, start=1):
            label = tk.Label(
                self.choice_mode_frame,
                text=text,
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
            label.bind("<Enter>", lambda event: event.widget.configure(bg=TEXT_COLOR, fg=BACKGROUND))
            label.bind("<Leave>", lambda event: event.widget.configure(bg=BACKGROUND, fg=TEXT_COLOR))
            self.choice_labels.append(label)

    def _create_input_mode(self):
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
        self.text_input.insert(0, "Name eingeben")
        self.text_input.configure(state="disabled")

    def show_choice_layout(self):
        self.choice_mode_frame.tkraise()

    def show_input_layout(self):
        self.input_mode_frame.tkraise()

    def show_empty_choices_layout(self):
        self.empty_choices_frame.tkraise()

    def _create_character_details(self):
        box = self._create_box(0, 1, "Charakter")
        box.columnconfigure(0, weight=1)

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

        self.character_details = tk.Label(
            box,
            text="\n".join(details),
            anchor="nw",
            justify="left",
            bg=PANEL_BACKGROUND,
            fg=TEXT_COLOR,
            font=DETAIL_FONT,
        )
        self.character_details.grid(row=0, column=0, sticky="nsew")

    def _create_reserved_area(self):
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

    def run(self):
        self.root.mainloop()


def create_ui(game=None):
    return Ui(game)


if __name__ == "__main__":
    create_ui().run()
