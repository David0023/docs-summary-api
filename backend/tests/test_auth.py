import pytest
from tests.conftest import app

@pytest.mark.asyncio
async def test_create_user(client):
    # Missing fields
    res = await client.post("/auth/register", json={
        "email": "user01",
        "password": "user01",
    })
    assert res.status_code == 422

    # Wrong email
    res = await client.post("/auth/register", json={
        "username": "user01",
        "email": "user01",
        "password": "user01",
    })
    assert res.status_code == 400