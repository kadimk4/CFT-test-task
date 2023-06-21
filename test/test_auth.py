
from conftest import client


def test_register():

    response = client.post('/auth/register', json={
        "email": "user@example.com",
        "password": "string",
        "first_name": "string",
        "last_name": "string"
    }
    )

    assert response.status_code == 201