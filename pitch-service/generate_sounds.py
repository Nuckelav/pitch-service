import numpy as np
import soundfile as sf
import os

os.makedirs("sounds", exist_ok=True)

notes = {
    "D3": 146.83,
    "D#3": 155.56,
    "E3": 164.81
}

duration = 1.2
sr = 44100

for name, freq in notes.items():
    t = np.linspace(0, duration, int(sr * duration), False)

    # som mais rico (menos "bip")
    wave = (
        0.5 * np.sin(2 * np.pi * freq * t) +
        0.3 * np.sin(2 * np.pi * freq * 2 * t) +
        0.2 * np.sin(2 * np.pi * freq * 3 * t)
    )

    # normalizar
    wave = wave / np.max(np.abs(wave))

    # fade in e fade out
    fade_len = int(0.2 * len(wave))

    fade_in = np.linspace(0, 1, fade_len)
    fade_out = np.linspace(1, 0, fade_len)

    wave[:fade_len] *= fade_in
    wave[-fade_len:] *= fade_out

    sf.write(f"sounds/{name}.wav", wave, sr)

print("Sons melhorados gerados!")