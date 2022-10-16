import json
import os

import boto3


def lambda_handler(event, context):
    """Body expected:
    {
        "summary": "Action Name",
        "description": "Action Description",
        "priority": "High"
    }
    """
    print(event)

    if not event["body"] or event["body"] == "":
        return {"statusCode": 400, "headers": {}, "body": "Bad Request"}

    action: dict[str, str] = json.loads(event["body"])

    search_params = {
        "id": event["pathParameters"]["id"],
        "created_dt": event["pathParameters"]["date"],
    }

    try:
        db_response = dynamo_table().update_item(
            Key=search_params,
            UpdateExpression="set summary=:s, description=:d, priority=:p",
            ExpressionAttributeValues={
                ":s": action["summary"],
                ":d": action["description"],
                ":p": action["priority"],
            },
            ConditionExpression="attribute_exists(id) and attribute_exists(created_dt)",
            ReturnValues="ALL_NEW",
        )
        print(db_response)

        return {
            "statusCode": 200,
            "headers": {},
            "body": json.dumps(db_response["Attributes"]),
        }

    except Exception as e:
        print(e)
        return {"statusCode": 400, "headers": {}, "body": "Bad Request"}


def dynamo_table():
    table_name = os.environ.get("TABLE", "Actions")
    region = os.environ.get("REGION", "eu-west-1")
    aws_environment = os.environ.get("AWSENV", "AWS")

    if aws_environment == "AWS_SAM_LOCAL":
        actions_table = boto3.resource("dynamodb", endpoint_url="http://dynamodb:8000")
    else:
        actions_table = boto3.resource("dynamodb", region_name=region)

    return actions_table.Table(table_name)
