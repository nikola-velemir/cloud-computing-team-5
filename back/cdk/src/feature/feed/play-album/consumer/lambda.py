import os
import json
from datetime import datetime, timezone

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["FEED_TABLE_NAME"])


def lambda_handler(event, context):
    event_type = event.get("type")
    payload = event.get("payload") or {}
    user_id = payload.get("userId")

    if not user_id:
        raise ValueError("Missing userId in payload")

    now = datetime.now(timezone.utc)
    now_ts = int(now.timestamp())

    if event_type == "PLAY_ALBUM":
        tracks = payload.get("tracks", [])

        for track in tracks:
            song_id = track.get("Id")
            name = track.get("Name")
            cover_image = track.get("CoverPath")
            if not song_id:
                continue

            existing = table.get_item(
                Key={"PK": f"USER#{user_id}", "SK": f"SONG#{song_id}"}
            ).get("Item")

            if existing:
                last_played = existing["LastTimePlay"]
                old_score = existing["Score"]
                hours_diff = max(1, (now_ts - last_played) / 3600.0)
                delta_score = 100 * (1 / hours_diff)
                new_score = old_score + delta_score

                table.update_item(
                    Key={"PK": f"USER#{user_id}", "SK": f"SONG#{song_id}"},
                    UpdateExpression="SET Score = :s, LastTimePlay = :t",
                    ExpressionAttributeValues={
                        ":s": new_score,
                        ":t": now_ts
                    }
                )
            else:
                table.put_item(
                    Item={
                        "PK": f"USER#{user_id}",
                        "SK": f"SONG#{song_id}",
                        "EntityType": "SONG",
                        "LastTimePlay": now_ts,
                        "Score": 100.0,
                        "Content": {
                            "ContentId": song_id,
                            "CoverImage": cover_image,
                            "Name": name
                        }
                    }
                )

        resp = table.query(
            KeyConditionExpression=Key("PK").eq(f"USER#{user_id}")
        )
        items = resp.get("Items", [])
        if len(items) > 20:
            items_sorted = sorted(items, key=lambda x: x["Score"])
            for item_to_delete in items_sorted[:len(items_sorted)-20]:
                table.delete_item(
                    Key={
                        "PK": item_to_delete["PK"],
                        "SK": item_to_delete["SK"]
                    }
                )

    return {"status": "ok"}
