# todo-list-api

## What's this?
An application that I'm using to learn about AWS and software engineering in general.

It will be a simple To-Do List API following a CRUD approach with the following resources:
- Amazon HTTP API Gateway: as the main entrypoint
- AWS Lambda: all the business code will run over this serverless solution
- DynamoDB: our NoSQL database

I'm trying to do a commit for each major change:
- `76edcf8ae38c782f77258be61f285b73a0ad1f74` - the inital CRUD application that is completely functional and ready to work
- `5fb7fc87b6984ffad3b35560e5873bae50d32ec0` - added CORS support and a mini Web Application to test it
- `18d2426ca23ce689d39d6f24618f30ce7f313076` - use Lambda Layers for reusable code

## How To's

Create docker network:

```bash
docker network create lambda-local
```

Create the dynamodb container:

```bash
docker run -p 8000:8000 -d --rm --network lambda-local --name dynamodb -v {your-user-root-folder}/.docker/dynamodb:/data/ amazon/dynamodb-local -jar DynamoDBLocal.jar -sharedDb -dbPath /data
```

Run the local SAM template API:

```bash
sam local start-api --docker-network lambda-local --parameter-overrides AWSENV=AWS_SAM_LOCAL
```

Run the unit tests:

```bash
python3 -m unittest discover tests/unit/ -bv
```

Validate the SAM template:

```bash
sam validate
```

Build the SAM stack:

```bash
sam build
```

Deploy the SAM stack:

```bash
sam deploy --guided
```

Delete the SAM stack:

```bash
sam delete --stack-name todo-list-api
```
