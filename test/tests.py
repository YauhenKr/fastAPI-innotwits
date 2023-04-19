from fastapi.testclient import TestClient
from main import app


test_client = TestClient(app)


def test_get_data_from_db(dynamodb_table, token):
    dynamodb_table.put_item(
        Item=dict(
            user_id=1,
            page_id=2,
            posts_count=5,
            likes_count=3,
            followers_count=2,
        )
    )
    endpoint = f"http://localhost:8001/get-statistic/2"

    response = test_client.get(
        url=endpoint,
        headers={'Authorization': f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_auth_with_valid_token(token):
    headers = {"Authorization": f"Bearer {token}"}
    endpoint = f"http://localhost:8001/get-statistic/2"
    response = test_client.get(url=endpoint, headers=headers)
    assert response.status_code == 200


def test_auth_with_expired_token(invalid_token):
    headers = {"Authorization": f"Bearer {invalid_token}"}
    endpoint = f"http://localhost:8001/get-statistic/2"
    response = test_client.get(url=endpoint, headers=headers)

    assert response.status_code == 401
