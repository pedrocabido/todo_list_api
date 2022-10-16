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


def dynamo_table():
    table_name = os.environ.get("TABLE", "Actions")
    region = os.environ.get("REGION", "eu-west-1")
    aws_environment = os.environ.get("AWSENV", "AWS")

    if aws_environment == "AWS_SAM_LOCAL":
        actions_table = boto3.resource("dynamodb", endpoint_url="http://dynamodb:8000")
    else:
        actions_table = boto3.resource("dynamodb", region_name=region)

    return actions_table.Table(table_name)
