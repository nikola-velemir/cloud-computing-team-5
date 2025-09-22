import os
import json
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

# Global model variables
demucs_model = None
whisper_model = None


def load_models():
    """Load models on first invocation"""
    global demucs_model, whisper_model

    if demucs_model is None:
        print("Loading Demucs model...")
        demucs_model = get_model(name="mdx_extra_q").eval()

    if whisper_model is None:
        print("Loading Whisper model...")
        whisper_model = whisper.load_model("small", device="cpu")


def lambda_handler(event, context):
    try:
        # Load models if not already loaded
        load_models()

        for record in event["Records"]:
            s3_info = record["s3"]
            bucket = s3_info["bucket"]["name"]
            key = unquote_plus(s3_info["object"]["key"])
            song_id = key.split("/")[0]

            print(f"Processing {key} from bucket {bucket}")

            # Download file locally
            input_path = f"/tmp/{os.path.basename(key)}"
            s3.download_file(bucket, key, input_path)

            # Create output folder
            output_dir = "/tmp/output"
            os.makedirs(output_dir, exist_ok=True)

            # Load and process audio
            print("Loading audio...")
            waveform, sr = torchaudio.load(input_path)

            # Ensure stereo input for Demucs
            if waveform.shape[0] == 1:
                waveform = waveform.repeat(2, 1)

            print("Running Demucs separation...")
            sources = apply_model(
                demucs_model,
                waveform.unsqueeze(0),  # Add batch dimension
                device="cpu",
                shifts=1,  # Reduce for faster processing
                overlap=0.25
            )

            # Extract vocals (index 3 in demucs output: drums, bass, other, vocals)
            vocals = sources[0, 3]  # [batch, source, channels, time]

            # Save vocals
            vocals_file = os.path.join(output_dir, "vocals.wav")
            torchaudio.save(vocals_file, vocals, sr)

            # Upload separated vocals to S3
            vocals_s3_key = f"{song_id}/vocals/vocals.wav"
            s3.upload_file(vocals_file, bucket, vocals_s3_key)
            print(f"Uploaded vocals to {vocals_s3_key}")

            # Transcribe vocals using Whisper
            print("Transcribing vocals...")
            result = whisper_model.transcribe(
                vocals_file,
                language="en",  # Specify language for faster processing
                fp16=False  # CPU doesn't support fp16
            )

            # Save and upload transcription
            lyrics_data = {
                "language": result.get("language", "en"),
                "transcription": result["text"],
                "segments": result.get("segments", [])
            }

            lyrics_file = os.path.join(output_dir, "lyrics.json")
            with open(lyrics_file, "w") as f:
                json.dump(lyrics_data, f, indent=2)

            lyrics_s3_key = f"{song_id}/lyrics/lyrics.json"
            s3.upload_file(lyrics_file, bucket, lyrics_s3_key)
            print(f"Uploaded transcription to {lyrics_s3_key}")

            # Cleanup temp files
            os.remove(input_path)
            os.remove(vocals_file)
            os.remove(lyrics_file)

            print(f"Successfully processed song {song_id}")

        return {
            "statusCode": 200,
            "body": json.dumps("Processing completed successfully")
        }

    except Exception as e:
        print(f"Error processing: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error: {str(e)}")
        }