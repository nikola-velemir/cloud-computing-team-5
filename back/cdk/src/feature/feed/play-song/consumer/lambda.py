import os
import json
import time
from datetime import datetime, timezone

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["FEED_TABLE"])

def lambda_handler(event, context):
    payload = event.get("body") or {}
    user_id = payload.get("userId")
    song_id = payload.get("entityId")
    song_name = payload.get("name")

    if not user_id or not song_id:
        raise ValueError("Missing userId or songId in payload")

    now = datetime.now(timezone.utc)
    now_ts = int(now.timestamp())

    existing = table.get_item(
        Key={"PK": f"USER#{user_id}", "SK": f"SONG#{song_id}"}
    ).get("Item")

    if existing:
        last_played = existing["LastPlayed"]
        old_score = existing["Score"]
        hours_diff = max(1, (now_ts - last_played) / 3600.0)
        delta_score = 100 * (1 / hours_diff)
        new_score = old_score + delta_score

        table.update_item(
            Key={"PK": f"USER#{user_id}", "SK": f"SONG#{song_id}"},
            UpdateExpression="SET Score = :s, LastPlayed = :t",
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
                    "CoverImage": payload.get("coverImage"),
                    "Name": song_name
                }
            }
        )

        resp = table.query(
            KeyConditionExpression=Key("PK").eq(f"USER#{user_id}")
        )
        items = resp.get("Items", [])

        if len(items) > 20:
            min_item = min(items, key=lambda x: x["Score"])
            table.delete_item(
                Key={
                    "PK": min_item["PK"],
                    "SK": min_item["SK"]
                }
            )

    return {"status": "ok"}
