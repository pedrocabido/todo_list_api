import json
from unittest import main, TestCase, mock
import os

import boto3
from moto import mock_dynamodb


@mock.patch.dict(
    os.environ, {"TABLE": "Mock_Actions", "REGION": "eu-west-1", "AWSENV": "MOCK"}
)
@mock_dynamodb
class TestCreateAction(TestCase):
    def setUp(self):
        self.dynamodb = boto3.client("dynamodb", region_name="eu-west-1")
        self.dynamodb.create_table(
            TableName="Mock_Actions",
            KeySchema=[
                {"AttributeName": "id", "KeyType": "HASH"},
                {"AttributeName": "created_dt", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "S"},
                {"AttributeName": "created_dt", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )

    def tearDown(self) -> None:
        self.dynamodb.delete_table(TableName="Mock_Actions")

    def test_create_action_201(self):
        from src.create_action import app

        event_data = "tests/test_events/create_action.json"
        with open(event_data, "r") as f:
            event = json.load(f)

        response = app.lambda_handler(event, "")
        body = json.loads(response["body"])

        self.assertEqual(response["statusCode"], 201)
        self.assertEqual(body["summary"], "Mock Action")
        self.assertEqual(body["description"], "Mock Description")
        self.assertEqual(body["priority"], "Mock Priority")

    def test_create_action_400(self):
        from src.create_action import app

        event_data = "tests/test_events/create_action.json"
        with open(event_data, "r") as f:
            event = json.load(f)
        event["body"] = ""

        response = app.lambda_handler(event, "")

        self.assertEqual(response["statusCode"], 400)
        self.assertEqual(response["body"], "Bad request")


if __name__ == "__main__":
    main()
