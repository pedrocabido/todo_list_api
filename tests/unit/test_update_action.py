import json
from unittest import main, TestCase, mock
import os

import boto3
from moto import mock_dynamodb


@mock.patch.dict(
    os.environ, {"TABLE": "Mock_Actions", "REGION": "eu-west-1", "AWSENV": "MOCK"}
)
@mock_dynamodb
class TestUpdateAction(TestCase):
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

    def test_update_action_200(self):
        mock_item = {
            "id": {"S": "12345-12345-12345-12345"},
            "created_dt": {"S": "2000-01-01 00:00:00.000000"},
            "summary": {"S": "Mock Action"},
            "description": {"S": "Mock Description"},
            "priority": {"S": "Mock Priority"},
        }
        self.dynamodb.put_item(TableName="Mock_Actions", Item=mock_item)
        from src.update_action import app

        event_data = "tests/test_events/update_action.json"
        with open(event_data, "r") as f:
            event = json.load(f)

        response = app.lambda_handler(event, "")
        body = json.loads(response["body"])

        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(body["summary"], "Mock Action Updated")
        self.assertEqual(body["description"], "Mock Description Updated")
        self.assertEqual(body["priority"], "Mock Priority")

    def test_update_action_400_wrong_id(self):
        mock_item = {
            "id": {"S": "67890-67890-67890-67890"},
            "created_dt": {"S": "2000-01-01 00:00:00.000000"},
            "summary": {"S": "Mock Action"},
            "description": {"S": "Mock Description"},
            "priority": {"S": "Mock Priority"},
        }
        self.dynamodb.put_item(TableName="Mock_Actions", Item=mock_item)
        from src.update_action import app

        event_data = "tests/test_events/update_action.json"
        with open(event_data, "r") as f:
            event = json.load(f)

        response = app.lambda_handler(event, "")

        self.assertEqual(response["statusCode"], 400)
        self.assertEqual(response["body"], "Bad Request")

    def test_update_action_400_wrong_date(self):
        mock_item = {
            "id": {"S": "12345-12345-12345-12345"},
            "created_dt": {"S": "9999-01-01 00:00:00.000000"},
            "summary": {"S": "Mock Action"},
            "description": {"S": "Mock Description"},
            "priority": {"S": "Mock Priority"},
        }
        self.dynamodb.put_item(TableName="Mock_Actions", Item=mock_item)
        from src.update_action import app

        event_data = "tests/test_events/update_action.json"
        with open(event_data, "r") as f:
            event = json.load(f)

        response = app.lambda_handler(event, "")

        self.assertEqual(response["statusCode"], 400)
        self.assertEqual(response["body"], "Bad Request")

    def test_update_action_400_no_body(self):
        mock_item = {
            "id": {"S": "12345-12345-12345-12345"},
            "created_dt": {"S": "2000-01-01 00:00:00.000000"},
            "summary": {"S": "Mock Action"},
            "description": {"S": "Mock Description"},
            "priority": {"S": "Mock Priority"},
        }
        self.dynamodb.put_item(TableName="Mock_Actions", Item=mock_item)
        from src.update_action import app

        event_data = "tests/test_events/update_action.json"
        with open(event_data, "r") as f:
            event = json.load(f)

        event["body"] = ""
        response = app.lambda_handler(event, "")

        self.assertEqual(response["statusCode"], 400)
        self.assertEqual(response["body"], "Bad Request")


if __name__ == "__main__":
    main()
