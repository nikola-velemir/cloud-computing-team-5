import os
import json
from datetime import datetime, timezone

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["FEED_TABLE"])


def lambda_handler(event, context):
    event_type = event.get("type")
    payload = event.get("body") or {}
    user_id = payload.get("userId")
    album_id = payload.get("entityId")

    if not user_id:
        raise ValueError("Missing userId in payload")

    now = datetime.now(timezone.utc)
    now_ts = int(now.timestamp())

    if event_type == "PLAY_ALBUM":

        if album_id:
            album_name = payload.get("name")
            album_cover = payload.get("coverImage")
            existing_album = table.get_item(
                Key={"PK": f"USER#{user_id}", "SK": f"ALBUM#{album_id}"}
            ).get("Item")

            if existing_album:
                if "lastTimePlay" in existing_album:
                    last_played = int(existing_album["lastTimePlay"])
                else:
                    last_played = now_ts
                old_score = existing_album["score"]
                hours_diff = max(1, (now_ts - last_played) / 3600.0)
                delta_score = 150 * (1 / hours_diff)
                new_score = old_score + int(delta_score)

                table.update_item(
                    Key={"PK": f"USER#{user_id}", "SK": f"ALBUM#{album_id}"},
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
                        "SK": f"ALBUM#{album_id}",
                        "entityType": "ALBUM",
                        "lastTimePlay": now_ts,
                        "score": 100,
                        "Content": {
                            "ContentId": album_id,
                            "ImagePath": album_cover,
                                "Name": album_name
                        }
                    }
                )

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
                if "lastTimePlay" in existing:
                    last_played = int(existing_album["lastTimePlay"])
                else:
                    last_played = now_ts
                old_score = existing["score"]
                hours_diff = max(1, (now_ts - last_played) / 3600.0)
                delta_score = 100 * (1 / hours_diff)
                new_score = old_score + int(delta_score)

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
                        "entityType": "SONG",
                        "lastTimePlay": now_ts,
                        "score": 100,
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
