import soundfile as sf
import numpy as np
import os

# sequência de notas (pode mudar depois)
notes = ["D3", "D#3", "E3", "D3"]

audio = []

for note in notes:
    file_path = f"sounds/{note}.wav"
    
    if os.path.exists(file_path):
        data, sr = sf.read(file_path)
        audio.extend(data)

# converter para array
audio = np.array(audio)

# salvar resultado
sf.write("output.wav", audio, sr)

print("Música criada: output.wav")