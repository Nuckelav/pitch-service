
import os
import tempfile
import numpy as np
import librosa
import soundfile as sf
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from collections import Counter

app = Flask(__name__)

# 🔥 LIBERA CORS (resolve erro de conexão)
CORS(app, resources={r"/*": {"origins": "*"}})


# =========================
# NOTA → FREQUÊNCIA
# =========================
def note_to_freq(note):
    mapping = {
        "C": 0, "C#": 1, "D": 2, "D#": 3,
        "E": 4, "F": 5, "F#": 6, "G": 7,
        "G#": 8, "A": 9, "A#": 10, "B": 11
    }

    try:
        if len(note) == 3:
            key = note[:2]
            octave = int(note[2])
        else:
            key = note[0]
            octave = int(note[1])

        n = mapping[key] + (octave - 4) * 12
        return 440 * (2 ** (n / 12))
    except:
        return 440


# =========================
# TESTE RÁPIDO
# =========================
@app.route("/")
def home():
    return "API OK"


# =========================
# PROCESSAR ÁUDIO
# =========================
@app.route("/process-audio", methods=["POST"])
def process_audio():
    try:
        if "audio" not in request.files:
            return jsonify({"error": "no audio file"}), 400

        file = request.files["audio"]

        # salvar arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            file.save(tmp.name)
            file_path = tmp.name

        # 🔥 PROTEÇÃO CONTRA CRASH DO LIBROSA
        try:
            y, sr = librosa.load(file_path, sr=22050)
        except Exception:
            sr = 44100
            y = np.zeros(sr)

        # detectar pitch
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_values = pitches[pitches > 0]

        raw_notes = [librosa.hz_to_note(p) for p in pitch_values[:120]]

        # limpar ruído
        notes = []
        step = 6

        for i in range(0, len(raw_notes), step):
            chunk = raw_notes[i:i + step]
            if chunk:
                most_common = Counter(chunk).most_common(1)[0][0]
                notes.append(most_common)

        if not notes:
            notes = ["D3", "E3", "D#3"]

        # gerar melodia
        sr_final = 44100
        melody = []

        for note in notes:
            freq = note_to_freq(note)
            t = np.linspace(0, 0.4, int(sr_final * 0.4), False)
            wave = 0.2 * np.sin(2 * np.pi * freq * t)
            melody.extend(wave)

        melody = np.array(melody)

        # fallback
        if len(melody) == 0:
            t = np.linspace(0, 2, sr_final, False)
            melody = 0.2 * np.sin(2 * np.pi * 440 * t)

        # normalizar
        max_val = np.max(np.abs(melody))
        if max_val > 0:
            melody = melody / max_val

        # salvar saída
        output_path = os.path.join(tempfile.gettempdir(), "output.wav")
        sf.write(output_path, melody, sr_final)

        return send_file(output_path, mimetype="audio/wav")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# RUN (Railway)
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))