import jwt
from jwt import decode, PyJWKClient
import requests
import os

COGNITO_POOL_ID = 'eu-central-1_TTH9eq5eX'
COGNITO_REGION = 'eu-central-1'
CLIENT_ID = '2bhb4d2keh19gbj25tuild6ti1'
JWKS_URL = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_POOL_ID}/.well-known/jwks.json"

JWKS = requests.get(JWKS_URL).json()


def verify_user_groups(headers: dict, allowed_groups: list):
    auth_header = headers.get("Authorization", "")
    if not auth_header:
        raise Exception("Missing Authorization header")

    token = auth_header.replace("Bearer ", "")
    jwk_client = PyJWKClient(JWKS_URL)
    signing_key = jwk_client.get_signing_key_from_jwt(token)

    try:

        decoded = decode(
            token,
            key=signing_key.key,
            algorithms=["RS256"],
            audience=CLIENT_ID
        )

        user_groups = decoded.get("cognito:groups", [])
        if not any(group in allowed_groups for group in user_groups):
            raise Exception("User not authorized")
        return decoded
    except Exception as e:
        raise Exception(f"Authorization failed: {str(e)}")

