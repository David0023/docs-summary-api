import pytest
from tests.conftest import app
from fastapi import status

@pytest.mark.asyncio
async def test_create_user(client):
    # Missing fields 422
    res = await client.post("/auth/register", json={
        "email": "user01",
        "password": "user01",
    })
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    # Wrong email format 400
    res = await client.post("/auth/register", json={
        "username": "user01",
        "email": "user01",
        "password": "user01",
    })
    assert res.status_code == status.HTTP_400_BAD_REQUEST

    # Valid user creation 201
    res = await client.post("/auth/register", json={
        "username": "user01",
        "email": "user01@gmail.com",
        "password": "user01",
    })
    assert res.status_code == status.HTTP_201_CREATED

    # Duplicate user name 400
    res = await client.post("/auth/register", json={
        "username": "user01",
        "email": "user02@gmail.com",
        "password": "user02",
    })
    assert res.status_code == status.HTTP_400_BAD_REQUEST

    # Duplicate email 400
    res = await client.post("/auth/register", json={
        "username": "user02",
        "email": "user01@gmail.com",
        "password": "user02",
    })
    assert res.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.asyncio
async def test_login(client):
    username = 'user01'
    email = 'user01@gmail.com'
    password = 'user01'
    
    await client.post("/auth/register", json={
        "username": username,
        "email": email,
        "password": password
    })

    # Wrong password login 401
    res = await client.post("/auth/login", data={
        'username': username,
        'password': password+'1'
    })
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

    # non-existent username login 401
    res = await client.post("/auth/login", data={
        'username': username+'1',
        'password': password
    })
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

    # Successful login 200
    res = await client.post("/auth/login", data={
        'username': username,
        'password': password
    })
    assert res.status_code == status.HTTP_200_OK


