from typing import TypedDict


class Choice(TypedDict):
    id: str
    label: str


class Scene:
    def __init__(self, scene_id: str, text: str, choices: list[Choice] | None = None) -> None:
        self.scene_id = scene_id
        self.text = text
        self.choices = choices or []
