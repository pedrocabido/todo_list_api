import json

from dynamo import dynamo_table


def lambda_handler(event, context):
    """Body optionally expected:
    {
        "lastKey": {
            "id": "2012396d-576d-4dcd-a093-ecc886a75eee",
            "created_dt": "2022-10-21 13:10:11.427197"
        }
    }
    """
    print(event)
    scan_params: dict[str, int | str] = {"Limit": 5}

    if event.get("body"):
        if last_key := json.loads(event["body"]).get("lastKey"):
            scan_params["ExclusiveStartKey"] = last_key

    try:
        actions_details = dynamo_table().scan(**scan_params)
        print(actions_details)

        response: dict[str, list | dict] = {"items": actions_details["Items"]}

        if last_key := actions_details.get("LastEvaluatedKey"):
            response["lastKey"] = last_key

        return {
            "statusCode": 200,
            "headers": {},
            "body": json.dumps(response),
        }

    except Exception as e:
        print(e)
        return {"statusCode": 500, "headers": {}, "body": "Internal Server Error"}
