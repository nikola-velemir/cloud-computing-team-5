import jwt
import requests
import os

COGNITO_POOL_ID = os.environ["USER_POOL_ID"]
COGNITO_REGION = os.environ["REGION"]
CLIENT_ID = os.environ["CLIENT_ID"]
JWKS_URL = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_POOL_ID}/.well-known/jwks.json"

JWKS = requests.get(JWKS_URL).json()


def verify_user_groups(headers: dict, allowed_groups: list):
    auth_header = headers.get("Authorization", "")
    if not auth_header:
        raise Exception("Missing Authorization header")

    token = auth_header.replace("Bearer ", "")

    try:
        header = jwt.get_unverified_header(token)
        key = next(k for k in JWKS['keys'] if k['kid'] == header['kid'])
        decoded = jwt.decode(
            token,
            key=jwt.algorithms.RSAAlgorithm.from_jwk(key),
            algorithms=['RS256'],
            audience=CLIENT_ID
        )
        user_groups = decoded.get("cognito:groups", [])
        if not any(group in allowed_groups for group in user_groups):
            raise Exception("User not authorized")
        return decoded
    except Exception as e:
        raise Exception(f"Authorization failed: {str(e)}")
