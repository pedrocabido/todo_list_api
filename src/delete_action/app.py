from dynamo import dynamo_table


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
