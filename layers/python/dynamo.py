import os

import boto3

def dynamo_table():
    table_name = os.environ.get("TABLE", "Actions")
    region = os.environ.get("REGION", "eu-west-1")
    aws_environment = os.environ.get("AWSENV", "AWS")

    if aws_environment == "AWS_SAM_LOCAL":
        actions_table = boto3.resource("dynamodb", endpoint_url="http://dynamodb:8000")
    else:
        actions_table = boto3.resource("dynamodb", region_name=region)

    return actions_table.Table(table_name)