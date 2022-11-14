import datetime
import json
import uuid

from dynamo import dynamo_table


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
