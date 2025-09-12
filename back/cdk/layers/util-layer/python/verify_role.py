def verify_user_groups(event: dict, allowed_groups: list):
    authorizer = event.get('requestContext', {}).get('authorizer', {})
    claims = authorizer.get('claims', {})
    if not claims:
        raise Exception("No claims found in requestContext.authorizer")

    user_groups = claims.get("cognito:groups", [])
    if isinstance(user_groups, str):
        user_groups = [user_groups]

    normalized_user_groups = [g.strip().lower() for g in user_groups]
    normalized_allowed = [g.strip().lower() for g in allowed_groups]

    if not any(g in normalized_allowed for g in normalized_user_groups):
        raise Exception(
            "User not authorized"
        )


    return claims