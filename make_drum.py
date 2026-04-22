import numpy as np
import soundfile as sf
import os

os.makedirs("drums", exist_ok=True)

sr = 44100

t = np.linspace(0, 0.2, int(sr * 0.2), False)
kick = 0.9 * np.sin(2 * np.pi * 60 * t) * np.exp(-10 * t)

sf.write("drums/kick.wav", kick, sr)

print("Kick criado!")