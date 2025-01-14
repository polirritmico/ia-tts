#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

import torch
from TTS.api import TTS

from text_processor import text_processor
from word_dict import word_dict

assert torch.cuda.is_available()
device = "cuda"

WORKDIR = "/tts/"


def text_to_audio(text: str, output_path: str, opts: dict):
    output_path = f"{WORKDIR}{output_path}"

    tts = TTS(
        model_name=opts.get("model"),
        config_path=opts.get("config_path"),
    ).to(device)

    tts_opts = {
        "file_path": output_path,
        "text": text,
        "speaker_wav": opts.get("speaker"),
        "vocoder_name": opts.get("vocoder"),
    }
    if opts.get("lang_model"):
        tts_opts["lang"] = opts.get("lang")

    # NOTE:
    # 1. Change config 20100 -> 19800 khz to improve the tempo (to fast):
    #    /home/docker-usr/.local/share/tts/tts_models--es--css10--vits/config.json
    # 2. pysbd is hardcoded to `en` so changed to `es`:
    #    ~/.local/lib/python3.10/site-packages/TTS/utils/synthesizer.py:93
    tts.tts_to_file(**tts_opts)
    return output_path


def process_file(file_path: str, output_file: str, opts):
    print("opening text file...")
    with open(file_path, "r", encoding="utf-8") as stream:
        content = stream.read()

    content = text_processor(content, word_dict, opts)

    print("Executing text to audio...")
    text_to_audio(content, output_file, opts)


def main():
    opts = {}
    tag = ""

    # Default
    # opts["model"] = "tts_models/en/ljspeech/tacotron2-DDC"
    # opts["vocoder"] = "vocoder_models/en/ljspeech/hifigan_v2"

    # opts["model"] = "jpgallegoar/F5-Spanish"

    # -------------------------------------------------------------------------
    # Picks

    # Universal ES
    opts["model"] = "tts_models/es/css10/vits"
    opts["vocoder"] = "vocoder_models/universal/libri-tts/wavegrad"
    opts["lang"] = "es"
    opts["lang_model"] = False
    # opts["vocoder"] = "vocoder_models/universal/libri-tts/fullband-melgan"

    # EN
    # opts["model"] = "tts_models/en/ljspeech/vits"
    # opts["vocoder"] = "vocoder_models/en/ljspeech/hifigan_v2"

    files = [
        "test_es2.txt",
        # "wool/Wool-29.txt",
        # "wool/Wool-30.txt",
    ]

    # -------------------------------------------------------------------------

    for file in files:
        print(f"Processing file {file}")
        output_file = f"{Path(file).stem}_{Path(opts.get('model')).name}{tag}.wav"
        process_file(file, output_file, opts)
        print("Done!")


if __name__ == "__main__":
    main()
