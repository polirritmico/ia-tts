SHELL = /bin/bash

.PHONY: speakers docker setup scripts

default: scripts run_tts

full: scripts speakers text run_tts

script: scripts
speaker: speakers

setup:
	pip install -r requirements.txt
	git clone https://github.com/idiap/coqui-ai-TTS && cd coqui-ai-TTS #&& pip install -e .

scripts:
	cp /models/Makefile ./Makefile
	cp /models/tts.py ./tts.py

run_tts:
	python3 tts.py

text:
	cp /models/*.txt ./
	cp /models/wool/*.txt ./wool/

speakers:
	cp /models/speakers/*.wav speakers/

docker:
	docker run -it --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --device=/dev/kfd --device=/dev/dri --group-add video --ipc=host --shm-size 8G --name tts -v ~/ia/tts:/tts rocm-tts
