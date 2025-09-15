import verify_role

def with_error_handling(allowed_groups):
    def decorator(handler):
        def wrapper(event, context):
            try:
                verify_role.verify_user_groups(event, allowed_groups)
                return handler(event, context)
            except Exception as e:
                return {
                    "statusCode": 403,
                    "body": str(e)
                }
        return wrapper
    return decorator
