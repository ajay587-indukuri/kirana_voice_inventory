import os
import tempfile
import json
import shutil
import imageio_ffmpeg
from dotenv import load_dotenv
from gnani.stt import GnaniSTTClient
from google import genai
from google.genai import types

# Configure FFmpeg executable path from imageio-ffmpeg for Vercel/serverless environments
ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
ffmpeg_dir = os.path.dirname(ffmpeg_path)

# Ensure an executable named 'ffmpeg' exists in PATH (imageio-ffmpeg names it e.g. ffmpeg-linux64-v...)
alias_path = os.path.join(ffmpeg_dir, "ffmpeg")
if not os.path.exists(alias_path):
    try:
        os.symlink(ffmpeg_path, alias_path)
    except Exception:
        tmp_bin = os.path.join(tempfile.gettempdir(), "bin")
        os.makedirs(tmp_bin, exist_ok=True)
        alias_path = os.path.join(tmp_bin, "ffmpeg")
        if not os.path.exists(alias_path):
            try:
                os.symlink(ffmpeg_path, alias_path)
            except Exception:
                shutil.copy2(ffmpeg_path, alias_path)
                os.chmod(alias_path, 0o755)
        ffmpeg_dir = tmp_bin

os.environ["PATH"] = (
    ffmpeg_dir
    + os.pathsep
    + os.environ.get("PATH", "")
)

load_dotenv()

GNANI_API_KEY = os.getenv(
    "GNANI_API_KEY",
    "vach_1ytE2CY5X2EPcyWd3KneQP25bJT1z0zvyVil882srHTkukqirmz3Xtp9foFFrl6eYjQK87XURyjW4WYXz9lpqVHDvo7Hj7gW_64f1ed2ac0ba7c161a4aed40ecd2da36",
)
gnani = GnaniSTTClient(api_key=GNANI_API_KEY)

gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
gemini = genai.Client(
    api_key=gemini_key,
    http_options={"api_version": "v1beta"}
)
client = gemini


def transcribe_audio(audio_file):
    extension = os.path.splitext(audio_file.filename)[1].lower()

    valid_extensions = [".m4a", ".wav", ".mp3", ".flac", ".ogg", ".aac", ".webm", ".mp4"]
    if extension not in valid_extensions:
        raise ValueError(f"Unsupported audio file format: {extension}")

    with tempfile.NamedTemporaryFile(suffix=extension, delete=False) as temp:
        temp.write(audio_file.read())
        temp_path = temp.name

    target_path = temp_path
    converted_path = None
    try:
        if extension in [".webm", ".mp4"]:
            import subprocess
            converted_path = temp_path + ".wav"
            subprocess.run(
                ["ffmpeg", "-y", "-i", temp_path, "-ar", "16000", "-ac", "1", converted_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
            target_path = converted_path

        result = gnani.transcribe(target_path, language_code="te-IN")
        return result["transcript"]
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        if converted_path and os.path.exists(converted_path):
            os.remove(converted_path)


def extract_order(transcript):
    schema = {
        "type": "OBJECT",
        "properties": {
            "items": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "name": {"type": "STRING"},
                        "quantity": {
                            "type": "NUMBER",
                            "nullable": True
                        },
                        "unit": {"type": "STRING"},
                        "clarification": {"type": "STRING"},
                    },
                    "required": [
                        "name",
                        "quantity",
                        "unit",
                        "clarification",
                    ],
                },
            }
        },
        "required": ["items"],
    }
    prompt = f"""
    You are ManaKirana AI, an assistant for Indian kirana shops.
    Understand the customer's grocery order.
    The transcript may contain Telugu, Tanglish or English.
    Extract every grocery product, its quantity and unit.

    Rules:
    - Understand Telugu grocery names and conversational language.
    - Return product names in simple English.
    - Convert spoken quantities into numbers.
    - Normalize units such as kg, g, litre, ml, packet and piece.
    - Do not invent products or quantities.
    - If quantity is unclear, use null.
    - If a product or quantity needs confirmation, explain it
      briefly in the clarification field.
    - Ignore greetings and unrelated conversation.

    Customer transcript:
    {transcript}
    """

    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=schema,
        ),
    )

    text = response.text.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    return json.loads(text)
