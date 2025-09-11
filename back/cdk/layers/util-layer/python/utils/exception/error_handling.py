def with_error_handling(handler):
    def wrapper(event, context):
        try:
            return handler(event, context)
        except Exception as e:
            return {
                "statusCode": 403,
                "body": str(e)
            }
    return wrapper