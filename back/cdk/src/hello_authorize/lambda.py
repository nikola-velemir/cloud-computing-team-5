import json

from cdk.src.feature.auth.verify_role import verify_user_groups


def lambda_handler(event, context):
    try:
        decoded_token = verify_user_groups(event['headers'], ["ADMIN"])
        # Ako je ovde, korisnik je autorizovan
        return {
            "statusCode": 200,
            "body": f"Hello, {decoded_token['username']}!"
        }
    except Exception as e:
        return {
            "statusCode": 403,
            "body": str(e)
        }
