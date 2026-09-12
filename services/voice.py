import sys

import numpy as np
import sounddevice as sd
import torch
import whisper


DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"[helix] loading Whisper on {DEVICE}...")
MODEL = whisper.load_model("small", device=DEVICE)
print("[helix] Whisper ready")


def listen(sample_rate=16000):
    chunks = []

    def callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)

        chunks.append(indata.copy())

    print("[helix] listening... press Enter to stop")

    with sd.InputStream(
        samplerate=sample_rate,
        channels=1,
        dtype="float32",
        callback=callback
    ):
        input()

    if not chunks:
        return ""

    audio = np.concatenate(chunks, axis=0).flatten()

    result = MODEL.transcribe(
        audio,
        fp16=(DEVICE == "cuda")
    )

    return result["text"].strip()