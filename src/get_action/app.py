import json
from dynamo import dynamo_table


def lambda_handler(event, context):
    print(event)
    action_id = event["pathParameters"]["id"]
    date = event["pathParameters"]["date"]

    try:
        action_details = dynamo_table().get_item(Key={"id": action_id, "created_dt": date})
        print(action_details)

        return {
            "statusCode": 200,
            "headers": {},
            "body": json.dumps(action_details["Item"]),
        }
    except Exception as e:
        print(e)
        return {
            "statusCode": 404,
            "headers": {},
            "body": "Not Found",
        }
