import argparse
import json
import re
import sys
from pathlib import Path


CONFIG_FILE_NAME = "export_config.json"
DATA_FILE_NAME = "data.json"
MAIN_FILE_NAME = "main.js"
MAX_REPLACEMENTS = 1
WORD_PRESET_NAME = "Word (.docx)"
WORD_PRESET_PATTERN = re.compile(r'"Word \(\.docx\)":\{.*?\},OpenOffice:', re.DOTALL)


def write_line(message):
    sys.stdout.write(f"{message}\n")


def load_word_preset(docx_dir):
    config_path = docx_dir / CONFIG_FILE_NAME
    with config_path.open("r", encoding="utf-8") as config_file:
        config = json.load(config_file)
    return config["wordPreset"]


def update_main_js(plugin_dir, word_preset):
    main_path = plugin_dir / MAIN_FILE_NAME
    source = main_path.read_text(encoding="utf-8")
    preset_js = json.dumps(word_preset, ensure_ascii=False, separators=(",", ":"))
    replacement = f'"{WORD_PRESET_NAME}":{preset_js},OpenOffice:'
    updated, count = WORD_PRESET_PATTERN.subn(replacement, source, count=MAX_REPLACEMENTS)
    if count != MAX_REPLACEMENTS:
        raise RuntimeError(f"Could not find the {WORD_PRESET_NAME} preset in {main_path}")
    if updated != source:
        main_path.write_text(updated, encoding="utf-8")
    return main_path


def update_data_json(plugin_dir, word_preset):
    data_path = plugin_dir / DATA_FILE_NAME
    if data_path.exists():
        with data_path.open("r", encoding="utf-8") as data_file:
            data = json.load(data_file)
    else:
        data = {"items": []}

    items = data.setdefault("items", [])
    for index, item in enumerate(items):
        if item.get("name") == WORD_PRESET_NAME:
            items[index] = dict(word_preset)
            break
    else:
        items.append(dict(word_preset))

    with data_path.open("w", encoding="utf-8") as data_file:
        json.dump(data, data_file, ensure_ascii=False, indent=2)
        data_file.write("\n")
    return data_path


def parse_args():
    parser = argparse.ArgumentParser(description="Install the DOCX export preset for obsidian-enhancing-export.")
    parser.add_argument(
        "--plugin-dir",
        default=Path(__file__).resolve().parents[1],
        type=Path,
        help="Path to the obsidian-enhancing-export plugin directory.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    docx_dir = Path(__file__).resolve().parent
    plugin_dir = args.plugin_dir.resolve()

    word_preset = load_word_preset(docx_dir)
    main_path = update_main_js(plugin_dir, word_preset)
    data_path = update_data_json(plugin_dir, word_preset)

    write_line(f"Updated {main_path}")
    write_line(f"Updated {data_path}")
    write_line("Reload Obsidian before exporting DOCX again.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        sys.stderr.write(f"Failed to install DOCX export preset: {error}\n")
        raise SystemExit(1)
