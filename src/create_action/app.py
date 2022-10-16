import datetime
import json
import os
import uuid

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
        return {"statusCode": 400, "headers": {}, "body": "Bad request"}

    action: dict[str, str] = json.loads(event["body"])

    params = {
        "id": str(uuid.uuid4()),
        "created_dt": str(datetime.datetime.now()),
        "summary": action["summary"],
        "description": action["description"],
        "priority": action["priority"],
    }

    try:
        db_response = dynamo_table().put_item(Item=params)
        print(db_response)

        return {"statusCode": 201, "headers": {}, "body": json.dumps(params)}
    except Exception as e:
        print(e)
        return {"statusCode": 500, "headers": {}, "body": "Internal Server Error"}


def dynamo_table():
    table_name = os.environ.get("TABLE", "Actions")
    region = os.environ.get("REGION", "eu-west-1")
    aws_environment = os.environ.get("AWSENV", "AWS")

    if aws_environment == "AWS_SAM_LOCAL":
        actions_table = boto3.resource("dynamodb", endpoint_url="http://dynamodb:8000")
    else:
        actions_table = boto3.resource("dynamodb", region_name=region)

    return actions_table.Table(table_name)
