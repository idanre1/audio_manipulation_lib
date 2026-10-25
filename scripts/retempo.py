#!/usr/bin/env python3
"""Detect each file's BPM and change its tempo to a target BPM, keeping pitch."""
import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np


def bpm_from_beats(beats):
    intervals = np.diff(beats)
    if len(intervals) == 0:
        raise ValueError("fewer than two beats detected")
    return 60 / float(np.median(intervals))


def run(*cmd):
    subprocess.run([str(c) for c in cmd], check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--to", type=float, required=True, help="target BPM")
    parser.add_argument("-o", "--out-dir", type=Path, required=True)
    parser.add_argument("--bitrate", default="256k", help="AAC bitrate")
    args = parser.parse_args()

    from beat_this.inference import File2Beats  # slow import; keeps --help fast

    detect = File2Beats(checkpoint_path="final0", device="cpu")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for src in args.files:
        dst = args.out_dir / f"{src.stem} - {args.to:g}bpm.m4a"
        if dst.exists():
            print(f"skip, exists: {dst}")
            continue
        with tempfile.TemporaryDirectory() as tmp:
            wav_in, wav_out, m4a = (Path(tmp, n) for n in ("in.wav", "out.wav", "out.m4a"))
            run("ffmpeg", "-nostdin", "-v", "error", "-i", src, "-c:a", "pcm_f32le", wav_in)
            bpm = bpm_from_beats(detect(str(wav_in))[0])
            ratio = args.to / bpm
            print(f"{src.name}: {bpm:.1f} -> {args.to:g} BPM (tempo x{ratio:.3f})", flush=True)
            run("rubberband", "-3", "-q", "--tempo", ratio, wav_in, wav_out)
            run("ffmpeg", "-nostdin", "-v", "error", "-i", wav_out, "-c:a", "aac", "-b:a", args.bitrate, m4a)
            shutil.move(m4a, dst)  # only finished files land in out-dir, so reruns skip safely


if __name__ == "__main__":
    main()
