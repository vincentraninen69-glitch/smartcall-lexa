import os
import requests
from flask import Flask, request, Response, send_from_directory
from twilio.twiml.voice_response import VoiceResponse
from datetime import datetime
from pathlib import Path
import openai
import uuid

app = Flask(__name__)

# === Ladda API-nycklar ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL")

openai.api_key = OPENAI_API_KEY

# === Mappar ===
MEDIA_DIR = Path("media")
RECORDINGS_DIR = Path("recordings")
MEDIA_DIR.mkdir(exist_ok=True)
RECORDINGS_DIR.mkdir(exist_ok=True)

# === Lexas personlighet ===
SYSTEM_PROMPT = (
    "Du är Lexa, en svensk kvinnlig AI-röstassistent från företaget Smart Call. "
    "Du är avslappnad men professionell, positiv och naturlig. "
    "Du hjälper företag att förstå hur Smart Calls AI-lösning fungerar genom att föra ett kort samtal. "
    "Hälsa alltid vänligt och svara naturligt på svenska. "
    "Du kan också ställa enkla frågor som 'Vad jobbar du med idag?' eller 'Vilken typ av samtal vill du automatisera?'. "
    "Om samtalet börjar ta slut, tacka och hänvisa till smartcall.ai. "
    "Avsluta alltid med ett varmt, proffsigt hejdå."
)


def download_file(url: str, dest_path: Path) -> Path:
    r = requests.get(url)
    r.raise_for_status()
    dest_path.write_bytes(r.content)
    return dest_path


def transcribe(file_path: Path) -> str:
    with open(file_path, "rb") as f:
        transcript = openai.Audio.transcriptions.create(model="whisper-1", file=f)
    return transcript.text


def chat_response(user_input: str) -> str:
    response = openai.Chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ],
        temperature=0.6,
        max_completion_tokens=200,
    )
    return response.choices[0].message["content"]


def synthesize_speech(text: str, output_path: Path):
    """Använd ElevenLabs för svensk kvinnlig röst"""
    voice_id = "pNInz6obpgDQGcFmaJgB"  # 'Elin' – naturlig svensk kvinnlig röst
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json",
    }
    data = {
        "text": text,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.8},
    }
    r = requests.post(url, headers=headers, json=data)
    r.raise_for_status()
    output_path.write_bytes(r.content)
    return output_path


@app.route("/voice", methods=["POST"])
def voice():
    """Första hälsningen när någon ringer"""
    vr = VoiceResponse()
    vr.say(
        "Hej! Du pratar med Lexa från Smart Call. "
        "Jag är en AI-röstassistent som hjälper företag att automatisera sina kundsamtal. "
        "Vill du testa hur jag fungerar?",
        language="sv-SE",
    )
    vr.record(
        action=f"{PUBLIC_BASE_URL}/process_recording",
        maxLength="20",
        playBeep=True,
        trim="trim-silence",
    )
    return Response(str(vr), mimetype="text/xml")


@app.route("/process_recording", methods=["POST"])
def process_recording():
    """Behandlar inspelningen och spelar upp Lexas svar"""
    recording_url = request.form.get("RecordingUrl")
    from_number = request.form.get("From")

    if not recording_url:
        resp = VoiceResponse()
        resp.say("Tyvärr, jag kunde inte höra något. Vill du prova igen?", language="sv-SE")
        return Response(str(resp), mimetype="text/xml")

    # Ladda ner inspelningen
    uid = uuid.uuid4().hex
    record_path = RECORDINGS_DIR / f"call_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    download_file(recording_url + ".wav", record_path)

    # Transkribera till text
    try:
        user_text = transcribe(record_path)
    except Exception as e:
        print("Transcription error:", e)
        user_text = "Ingen röst upptäcktes."

    print(f"Transkription ({from_number}): {user_text}")

    # Skapa Lexas svar
    try:
        response_text = chat_response(user_text)
    except Exception as e:
        print("ChatGPT error:", e)
        response_text = "Förlåt, jag fick problem att tänka ut ett svar just nu."

    print("Lexa svarar:", response_text)

    # Syntetisera svensk röst
    output_audio = MEDIA_DIR / f"reply_{uid}.mp3"
    synthesize_speech(response_text, output_audio)

    # Spela upp Lexas röst
    vr = VoiceResponse()
    vr.play(f"{PUBLIC_BASE_URL}/media/{output_audio.name}")
    vr.record(
        action=f"{PUBLIC_BASE_URL}/process_recording",
        maxLength="20",
        playBeep=True,
        trim="trim-silence",
    )
    return Response(str(vr), mimetype="text/xml")


@app.route("/media/<path:filename>")
def media(filename):
    return send_from_directory(str(MEDIA_DIR), filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
