#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
from pathlib import Path

from num2words import num2words

SYMBOLS = {
    "…": "...",
    "–": "-",
    "—": "-",
    "«": '"',
    "»": '"',
}


def replace_unhandled_symbols(line: str) -> str:
    for target, replacement in SYMBOLS.items():
        line = line.replace(target, replacement)
    return line


def add_missing_periods(line: str) -> str:
    pattern = r"[.!?…]$"
    if not re.search(pattern, line):
        return line + "."
    return line


def convert_numbers_to_words(line: str, lang: str) -> str:
    line = re.sub(r"\d+", lambda match: num2words(int(match.group(0)), lang=lang), line)
    return line


def apply_custom_replacement_dict(line: str, custom_dict: dict[str, str]) -> str:
    for target, replacement in custom_dict.items():
        line = line.replace(target, replacement)
    return line


def uppercase_first_letter(line: str) -> str:
    pattern = r"([a-záéíóúA-ZÁÉÍÓÚ])"
    line = re.sub(pattern, lambda char: char.group(1).upper(), line, 1)
    return line


def store_temp_text(text: str) -> None:
    tmpdir = Path("tmp")
    basename = "_text-processed_"

    tmpdir.mkdir(parents=True, exist_ok=True)
    for i in range(1, 999):
        file = tmpdir / f"{basename}{i:03d}.txt"
        if not file.exists():
            file.write_text(text, encoding="utf-8")


def text_processor(raw_text: str, replacement_dict: dict[str, str], opts: dict) -> str:
    print("Applying text filters and customizations...")

    processed: list[str] = []
    for line in raw_text.splitlines():
        if not line:
            continue

        line = add_missing_periods(line)
        line = convert_numbers_to_words(line, opts.get("lang"))
        line = replace_unhandled_symbols(line)
        line = apply_custom_replacement_dict(line, replacement_dict)
        line = uppercase_first_letter(line)

        processed.append(line)

    multiline_text = "\n\n".join(processed)
    store_temp_text(multiline_text)
    return multiline_text


def main():
    if len(sys.argv) < 1:
        raise ValueError("Missing input file")

    input_file = Path(sys.argv[1])
    output_file = input_file.stem + "_processed" + input_file.suffix
    opts = {"lang": sys.argv[2] if len(sys.argv) > 2 else "en"}
    from word_dict import word_dict

    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print(f"lang: {opts['lang']}")
    print(f"word_dict: '{word_dict}'")

    try:
        with open(input_file, "r", encoding="utf-8") as stream:
            raw_text = stream.read()
    except Exception as e:
        raise Exception(f"Error reading the file:\n{e}")

    processed_text = text_processor(raw_text, word_dict, opts)
    output_file.write_text(processed_text, encoding="utf-8")

    print("Done")


if __name__ == "__main__":
    main()
