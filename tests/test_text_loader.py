import tempfile
import unittest
from pathlib import Path

from src.Utils import format_text, get_text, load_text_blocks, require_text_keys


class TextLoaderTest(unittest.TestCase):
    def _write_text_file(self, content: str) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        file_path = Path(temp_dir.name) / "texts.txt"
        file_path.write_text(content, encoding="utf-8")
        return file_path

    def test_loads_multiple_blocks(self) -> None:
        file_path = self._write_text_file("[start]\nHallo\n\nWelt\n\n[end]\nEnde")

        texts = load_text_blocks(file_path)

        self.assertEqual(texts["start"], "Hallo\n\nWelt")
        self.assertEqual(texts["end"], "Ende")

    def test_rejects_text_before_first_key(self) -> None:
        file_path = self._write_text_file("Kaputter Anfang\n[start]\nText")

        with self.assertRaises(ValueError):
            load_text_blocks(file_path)

    def test_rejects_duplicate_key(self) -> None:
        file_path = self._write_text_file("[start]\nText\n[start]\nNoch ein Text")

        with self.assertRaises(ValueError):
            load_text_blocks(file_path)

    def test_rejects_invalid_header(self) -> None:
        file_path = self._write_text_file("[start\nText")

        with self.assertRaises(ValueError):
            load_text_blocks(file_path)

    def test_missing_file_raises_file_not_found(self) -> None:
        with self.assertRaises(FileNotFoundError):
            load_text_blocks(Path("fehlt.txt"))

    def test_get_text_rejects_missing_key(self) -> None:
        with self.assertRaises(KeyError):
            get_text({"start": "Text"}, "fehlt", "test")

    def test_format_text_rejects_missing_placeholder(self) -> None:
        with self.assertRaises(KeyError):
            format_text({"start": "Hallo {name}"}, "start", "test")

    def test_require_text_keys_rejects_missing_keys(self) -> None:
        with self.assertRaises(KeyError):
            require_text_keys({"start": "Text"}, ["start", "ende"], "test")


if __name__ == "__main__":
    unittest.main()
