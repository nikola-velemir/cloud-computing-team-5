import os
import uuid
from urllib.parse import unquote_plus
import boto3
import torchaudio
import torch
from demucs.pretrained import get_model
from demucs.apply import apply_model
import whisper

# Initialize S3 client
s3 = boto3.client("s3")

# Load models globally for Lambda warm start
demucs_model = get_model(name="demucs_quantized").eval()  # CPU-friendly
whisper_model = whisper.load_model("small")  # small = good balance speed/accuracy

def lambda_handler(event, _context):
    for record in event["Records"]:
        s3_info = record["s3"]
        bucket = s3_info["bucket"]["name"]
        key = unquote_plus(s3_info["object"]["key"])
        song_id = key.split("/")[0]
        ext = os.path.splitext(key)[1].lower()

        # Download file locally
        input_path = f"/tmp/{os.path.basename(key)}"
        s3.download_file(bucket, key, input_path)

        # Create output folder for separated vocals
        output_dir = "/tmp/output"
        os.makedirs(output_dir, exist_ok=True)

        # Load audio
        waveform, sr = torchaudio.load(input_path)

        # Run Demucs separation
        sources = apply_model(demucs_model, waveform, sr=sr, device="cpu", split=True, overlap=0)
        vocals = sources[0]  # vocals are first channel

        vocals_file = os.path.join(output_dir, "vocals.wav")
        torchaudio.save(vocals_file, vocals, sr)

        # Upload separated vocals to S3
        vocals_s3_key = f"{song_id}/vocals/{os.path.basename(vocals_file)}"
        s3.upload_file(vocals_file, bucket, vocals_s3_key)

        # Transcribe vocals using Whisper
        result = whisper_model.transcribe(vocals_file)

        # Upload transcription to S3
        lyrics_file = os.path.join(output_dir, "lyrics.json")
        with open(lyrics_file, "w") as f:
            import json
            json.dump({"language": result["language"], "transcription": result["text"]}, f)

        lyrics_s3_key = f"{song_id}/lyrics/lyrics.json"
        s3.upload_file(lyrics_file, bucket, lyrics_s3_key)

        print(f"Processed song {song_id}: vocals and transcription uploaded.")
