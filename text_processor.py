#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
from pathlib import Path

from num2words import num2words


def add_missing_periods(line: str) -> str:
    pattern = r"[.!?…]$"
    if not re.search(pattern, line):
        return line + "."
    return line


def convert_numbers_to_words(line: str, lang: str) -> str:
    line = re.sub(r"\d+", lambda match: num2words(int(match.group(0))), line)
    return line


def apply_custom_replacement_dict(line: str, custom_dict: dict[str, str]) -> str:
    for target, replacement in custom_dict.items():
        line = line.replace(target, replacement)
    return line


UNHANDLED_SYMBOLS = {
    "…": "...",
    "–": "-",
}


def replace_unhandled_symbols(line: str) -> str:
    for target, replacement in UNHANDLED_SYMBOLS.items():
        line = line.replace(target, replacement)
    return line


def process(raw_text: str, replacement_dict: dict[str, str], opts: dict) -> str:
    print("Applying processors...")

    processed: list[str] = []
    for line in raw_text.splitlines():
        if not line:
            continue

        line = add_missing_periods(line)
        line = convert_numbers_to_words(line, opts.get("lang"))
        line = replace_unhandled_symbols(line)
        line = apply_custom_replacement_dict(line, replacement_dict)

        processed.append(line)

    multiline_text = "\n".join(processed)
    return multiline_text


def main():
    if len(sys.argv) < 1:
        raise ValueError("Missing input file")
    opts = {}

    try:
        from .word_dict import word_dict
    except Exception:
        word_dict = {}

    input_file = Path(sys.argv[1])
    output_file = input_file.stem + "_processed" + input_file.suffix
    opts["lang"] = sys.argv[2] if len(sys.argv) > 2 else "en"

    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print(f"lang: {opts['lang']}")

    try:
        with open(input_file, "r", encoding="utf-8") as stream:
            raw_text = stream.read()
    except Exception as e:
        raise Exception(f"Error reading the file:\n{e}")

    processed_text = process(raw_text, word_dict, opts)

    with open(output_file, "w", encoding="utf-8") as stream:
        stream.write(processed_text)
    print("Done")


if __name__ == "__main__":
    main()
