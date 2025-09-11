


def lambda_handler(event, context):
    #decoded_token = verify_user_groups(event['headers'], ["ADMIN"])
    return {
        "statusCode": 200,
        #"body": f"Hello, {decoded_token['username']}!"
    }
