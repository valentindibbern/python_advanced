from __future__ import annotations

from pathlib import Path
import random
import re
from typing import TYPE_CHECKING

from src.Datatypes.Enums import Attributes, InputMode
from src.Datatypes.Models import AttributeCheck, Choice, PlayerData, GameMsgType, GameResponse

if TYPE_CHECKING:
    from src.Classes.Player import Player


TEXT_KEY_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+$")


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
        "goal_status": "",
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


def roll_d6() -> int:
    return random.randint(1, 6)


def make_attribute_check(player: Player, attribute: Attributes, difficulty: int) -> AttributeCheck:
    roll = roll_d6()
    attribute_value = player.attributes[attribute]
    total = roll + attribute_value
    return {
        "attribute": attribute,
        "attribute_label": attribute.get_label(),
        "difficulty": difficulty,
        "roll": roll,
        "attribute_value": attribute_value,
        "total": total,
        "success": total >= difficulty,
    }


def format_attribute_check(check: AttributeCheck) -> str:
    result = "Erfolg" if check["success"] else "Nicht genug"
    return (
        f"Probe auf {check['attribute_label']}:\n"
        f"W6 {check['roll']} + {check['attribute_label']} {check['attribute_value']} "
        f"= {check['total']} gegen Schwierigkeit {check['difficulty']}.\n"
        f"{result}."
    )


def load_text_blocks(file_path: Path) -> dict[str, str]:
    if not file_path.exists():
        raise FileNotFoundError(f"Textdatei nicht gefunden: {file_path}")
    if not file_path.is_file():
        raise ValueError(f"Textpfad ist keine Datei: {file_path}")

    texts: dict[str, str] = {}
    current_key = ""
    current_lines: list[str] = []

    for line_number, line in enumerate(file_path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped_line = line.strip()
        is_header = stripped_line.startswith("[") and stripped_line.endswith("]")

        if stripped_line.startswith("[") or stripped_line.endswith("]"):
            if not is_header:
                raise ValueError(
                    f"Ungültiger Textblock-Header in {file_path} Zeile {line_number}: {line}"
                )

        if is_header:
            if current_key != "":
                texts[current_key] = "\n".join(current_lines).strip()

            current_key = stripped_line[1:-1].strip()
            current_lines = []

            if current_key == "":
                raise ValueError(f"Leerer Textblock-Key in {file_path} Zeile {line_number}")
            if not TEXT_KEY_PATTERN.match(current_key):
                raise ValueError(
                    f"Ungültiger Textblock-Key in {file_path} Zeile {line_number}: {current_key}"
                )
            if current_key in texts:
                raise ValueError(
                    f"Doppelter Textblock-Key '{current_key}' in {file_path} Zeile {line_number}"
                )
            continue

        if current_key == "" and stripped_line != "":
            raise ValueError(f"Text vor dem ersten Textblock in {file_path} Zeile {line_number}")

        if current_key != "":
            current_lines.append(line)

    if current_key != "":
        texts[current_key] = "\n".join(current_lines).strip()

    return texts


def get_text(texts: dict[str, str], key: str, source: str = "") -> str:
    try:
        return texts[key]
    except KeyError as error:
        source_text = f" in {source}" if source else ""
        raise KeyError(f"Fehlender Textblock '{key}'{source_text}") from error


def format_text(texts: dict[str, str], key: str, source: str = "", **values: object) -> str:
    text = get_text(texts, key, source)
    try:
        return text.format(**values)
    except KeyError as error:
        missing_key = str(error).strip("'")
        source_text = f" aus {source}" if source else ""
        raise KeyError(
            f"Fehlender Platzhalter '{missing_key}' in Textblock '{key}'{source_text}"
        ) from error


def require_text_keys(texts: dict[str, str], required_keys: list[str], source: str) -> None:
    missing_keys = [key for key in required_keys if key not in texts]
    if missing_keys:
        missing_text = ", ".join(missing_keys)
        raise KeyError(f"Fehlende Textblöcke in {source}: {missing_text}")
