import os

import boto3


def lambda_handler(event, context):
    print(event)

    action_id: str = event["pathParameters"]["id"]
    action_date: str = event["pathParameters"]["date"]

    try:
        db_response = dynamo_table().delete_item(
            Key={"id": action_id, "created_dt": action_date},
            ConditionExpression="attribute_exists(id) and attribute_exists(created_dt)",
        )
        print(db_response)

        return {
            "statusCode": 200,
            "body": "Deleted with success",
        }
    except Exception as e:
        print(e)
        return {
            "statusCode": 400,
            "body": "Bad Request",
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
