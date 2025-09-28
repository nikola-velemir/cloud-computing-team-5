import os
import json
from urllib.parse import unquote_plus
import boto3
import whisper

# Initialize S3 client
s3 = boto3.client("s3")
MODEL_TYPE = os.environ.get("MODEL_TYPE", 'small')

# Global model variable
whisper_model = None
MODEL_PATH = f"/models/{MODEL_TYPE}.pt"  # Path to the model you copied


def load_models():
    """Load Whisper model on first invocation from local file"""
    global whisper_model
    if whisper_model is None:
        print(f"Loading Whisper model from {MODEL_PATH}...")
        whisper_model = whisper.load_model(MODEL_PATH, device="cpu")


def lambda_handler(event, context):
    try:
        load_models()

        for record in event["Records"]:
            s3_info = record["s3"]
            bucket = s3_info["bucket"]["name"]
            key = unquote_plus(s3_info["object"]["key"])
            file_id = os.path.basename(key).split(".")[0]
            song_id = key.split("/")[0]
            print(f"Processing {key} from bucket {bucket}")

            input_path = f"/tmp/{os.path.basename(key)}"
            s3.download_file(bucket, key, input_path)

            print("Transcribing audio...")
            result = whisper_model.transcribe(
                input_path,
            )

            # Save transcription
            output_dir = "/tmp/output"
            os.makedirs(output_dir, exist_ok=True)
            transcript_file = os.path.join(output_dir, f"{file_id}_transcript.json")

            lyrics_data = {
                "language": result.get("language", "en"),
                "transcription": result["text"],
                "segments": result.get("segments", [])
            }

            with open(transcript_file, "w") as f:
                json.dump(lyrics_data, f, indent=2)

            transcript_s3_key = f"{song_id}/lyrics/lyrics.json"
            s3.upload_file(transcript_file, bucket, transcript_s3_key)
            print(f"Uploaded transcription to {transcript_s3_key}")

            os.remove(input_path)
            os.remove(transcript_file)

            print(f"Successfully processed file {file_id}")

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