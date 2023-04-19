import jwt
import pytest
import boto3

from settings import config


@pytest.fixture(scope='module')
def dynamodb_table():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table_name = 'test_table'
    table = dynamodb.create_table(
                TableName=table_name,
                KeySchema=[
                    {"AttributeName": "user_id", "KeyType": "HASH"},
                    {"AttributeName": "page_id", "KeyType": "RANGE"},
                ],
                AttributeDefinitions=[
                    {"AttributeName": "user_id", "AttributeType": "N"},
                    {"AttributeName": "page_id", "AttributeType": "N"},
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
    )
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    yield table
    table.delete()


@pytest.fixture(scope="module")
def token():
    payload = {
        'user_id': 1,
        'username': "user.username",
        'exp': 10 * 43568984560934069830683408608
    }
    secret_key = config.SECRET_KEY
    algorithm = config.ALGORYTHM
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token


@pytest.fixture(scope="module")
def invalid_token():
    payload = {
        'user_id': 5,
        'username': "user.username_test",
        'exp': 0
    }
    secret_key = config.SECRET_KEY
    algorithm = config.ALGORYTHM
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token
