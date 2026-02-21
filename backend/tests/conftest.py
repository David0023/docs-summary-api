import os
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

# Ensure settings can be initialized during test imports.
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("OPENAI_API_KEY", "test-openai-api-key")

from main import app
from core.dependencies import get_db
from core.database import Base
from models import user, job, document

# Test engine
test_engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async def override_get_db():
        async with TestSessionLocal() as session:
            yield session
    
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

#-------------------- TODO: Make fixtures
@pytest_asyncio.fixture
async def auth_client(client):
    user_data = {
        'username': 'user01',
        'email': 'user01@domain.com',
        'password': 'user01pass'
    }
    await client.post('/auth/register', json=user_data)
    
    login_data = {
        'username': user_data['username'],
        'password': user_data['password']
    }
    res = await client.post('/auth/login', data=login_data)

    token = res.json()['access_token']
    client.headers.update({"Authorization": f"Bearer {token}"})

    yield client
    client.headers.pop("Authorization", None)
