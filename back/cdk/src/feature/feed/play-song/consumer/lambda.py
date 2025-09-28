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
        if "lastTimePlay" in existing:
            last_played = int(existing["lastTimePlay"])
        else:
            last_played = now_ts
        old_score = existing["score"]
        hours_diff = max(1, (now_ts - last_played) / 3600.0)
        delta_score = 100 * (1 / hours_diff)
        new_score = old_score + int(delta_score)

        table.update_item(
            Key={"PK": f"USER#{user_id}", "SK": f"SONG#{song_id}"},
            UpdateExpression="SET score = :s, lastTimePlay = :t, updatedAt = :u",
            ExpressionAttributeValues={
                ":s": new_score,
                ":t": now_ts,
                ":u": now.isoformat()
            }
        )

    else:
        table.put_item(
            Item={
                "PK": f"USER#{user_id}",
                "SK": f"SONG#{song_id}",
                "entityType": "SONG",
                "lastTimePlay": now_ts,
                "score": 100,
                "ImagePath": payload.get("coverImage"),
                "name": song_name,
                "updatedAt": now.isoformat()
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
