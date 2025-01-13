#!/usr/bin/env bash

# e - script stops on error (return !=0)
# u - error if undefined variable
# o pipefail - script fails if one of piped command fails
# x - output each line (debug)
set -euo pipefail

INPUT="$1"
OUTPUT="${INPUT%.wav}.mp3"
TEMP_FILE_1="${INPUT%.wav}-temp.wav"
TEMP_FILE_2="${INPUT%.wav}-temp2.wav"

echo -e "Source file: ${INPUT}"

echo "Adding wrap silences..."
sox "$INPUT" "$TEMP_FILE_1" pad 1 1

echo -e "Removing inner pauses..."
ffmpeg -i "${TEMP_FILE_1}" \
    -af "silenceremove=stop_periods=-1:stop_threshold=-40dB:stop_duration=0.8" \
    "${TEMP_FILE_2}"

echo -e "Converting to mp3..."
lame --preset standard "${TEMP_FILE_2}" "${OUTPUT}"

echo -e "Removing temp files..."
rm "${TEMP_FILE_1}"
rm "${TEMP_FILE_2}"

echo -e "Done"
