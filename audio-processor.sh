#!/usr/bin/env bash

# e - script stops on error (return !=0)
# u - error if undefined variable
# o pipefail - script fails if one of piped command fails
# x - output each line (debug)
set -euo pipefail

if [[ -z ${1-} ]]; then
    echo "Missing path or file"
    exit 1
fi

function process_audio_file() {
    INPUT="$1"
    OUTPUT="${INPUT%.wav}.mp3"
    TEMP_FILE_1="${INPUT%.wav}-temp.wav"
    TEMP_FILE_2="${INPUT%.wav}-temp2.wav"

    echo -e "-----------------------------\n- Processing: ${INPUT}"

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
}

file_list=""
audio_files=()

function get_files() {
    if [ -f "$1" ]; then
        file_list="$1"
    elif [ -d "$1" ]; then
        file_list=$(find "$1" -mindepth 1 -maxdepth 1 -type f)
    else
        echo "Invalid input"
        exit 1
    fi
}

function get_wav_files() {
    local audio_raw_list

    audio_raw_list=$(grep "\.wav$" <<<"$file_list" || true)
    audio_raw_list=$(sed "s|\./||g" <<<"$audio_raw_list")
    audio_raw_list=$(sort <<<"$audio_raw_list")

    mapfile -t audio_files <<<"$audio_raw_list"

    if [[ -z ${audio_files[0]} ]]; then
        echo "No wav audio file found"
        exit 1
    fi
}

get_files "$1"
get_wav_files
echo -e "Files to process: '${audio_files}'\n----------------------------------------------"

for ((i = 0; i < ${#audio_files[@]}; i++)); do
    file=${audio_files[i]}
    process_audio_file "$file"
done
