# audio_manipulation_lib

High-fidelity audio recipes for Linux using free tools: one script per task in `scripts/`. Scripts write AAC audio in `.m4a` files.

| Task | Libraries | Script |
|---|---|---|
| BPM detection | [Beat This!](https://github.com/CPJKU/beat_this) (PyTorch) | `scripts/retempo.py` |
| Tempo change, pitch kept | [Rubber Band](https://breakfastquay.com/rubberband/) R3 engine | `scripts/retempo.py` |
| Decode / encode | [FFmpeg](https://ffmpeg.org/) | all |

## Setup

```sh
sudo apt install ffmpeg rubberband-cli
uv sync
```

## Change a batch of files to a target BPM

```sh
uv run scripts/retempo.py --to 100 -o out/ fixtures/*.mp3
```

Each file's BPM is detected separately. Detected BPM is an estimate: half- or double-time errors happen, so listen to the results.

## Test

```sh
uv run pytest
```
