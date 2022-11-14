import json
import sys
from unittest import main, TestCase, mock
import os

import boto3
from moto import mock_dynamodb

last_key_body = '{\n    "lastKey": {\n        "date": "2000-01-01 00:00:00.000000",\n        "id": "12345-12345-12345-12345-4"\n    }\n}'


@mock.patch.dict(
    os.environ, {"TABLE": "Mock_Actions", "REGION": "eu-west-1", "AWSENV": "MOCK"}
)
@mock_dynamodb
class TestListActions(TestCase):
    def setUp(self):
        sys.path.append(os.getcwd() + '/layers/python')
        self.dynamodb = boto3.client("dynamodb", region_name="eu-west-1")
        self.dynamodb.create_table(
            TableName="Mock_Actions",
            KeySchema=[
                {"AttributeName": "id", "KeyType": "HASH"},
                {"AttributeName": "date", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "S"},
                {"AttributeName": "date", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )

        event_data = "tests/test_events/list_actions.json"
        with open(event_data, "r") as f:
            self.event = json.load(f)

    def tearDown(self) -> None:
        self.dynamodb.delete_table(TableName="Mock_Actions")
        sys.path.remove(os.getcwd() + '/layers/python')

    def test_list_action_200_without_pagination(self):
        number_of_items = 3
        for i in range(0, number_of_items):
            mock_item = {
                "id": {"S": f"12345-12345-12345-12345-{i}"},
                "date": {"S": "2000-01-01 00:00:00.000000"},
                "summary": {"S": f"Mock Action {i}"},
                "description": {"S": f"Mock Description {i}"},
                "priority": {"S": f"Mock Priority {i}"},
            }
            self.dynamodb.put_item(TableName="Mock_Actions", Item=mock_item)
        from src.list_actions import app

        response = app.lambda_handler(self.event, "")
        body = json.loads(response["body"])

        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(len(body["items"]), number_of_items)
        self.assertRaises(KeyError, lambda: body["lastKey"])

    def test_list_action_200_with_pagination_on_first_page(self):
        number_of_items = 7
        for i in range(0, number_of_items):
            mock_item = {
                "id": {"S": f"12345-12345-12345-12345-{i}"},
                "date": {"S": "2000-01-01 00:00:00.000000"},
                "summary": {"S": f"Mock Action {i}"},
                "description": {"S": f"Mock Description {i}"},
                "priority": {"S": f"Mock Priority {i}"},
            }
            self.dynamodb.put_item(TableName="Mock_Actions", Item=mock_item)
        from src.list_actions import app

        response = app.lambda_handler(self.event, "")
        body = json.loads(response["body"])

        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(len(body["items"]), 5)
        self.assertTrue(body["lastKey"])

    def test_list_action_200_with_pagination_on_last_page(self):
        number_of_items = 7
        for i in range(0, number_of_items):
            mock_item = {
                "id": {"S": f"12345-12345-12345-12345-{i}"},
                "date": {"S": "2000-01-01 00:00:00.000000"},
                "summary": {"S": f"Mock Action {i}"},
                "description": {"S": f"Mock Description {i}"},
                "priority": {"S": f"Mock Priority {i}"},
            }
            self.dynamodb.put_item(TableName="Mock_Actions", Item=mock_item)
        from src.list_actions import app

        self.event["body"] = last_key_body
        response = app.lambda_handler(self.event, "")
        body = json.loads(response["body"])

        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(len(body["items"]), 2)
        self.assertRaises(KeyError, lambda: body["lastKey"])


if __name__ == "__main__":
    main()
