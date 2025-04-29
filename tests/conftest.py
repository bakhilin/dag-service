import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from main import app
from src.db.session import get_db
from src.models.base import Base
from src.models.graph import GraphModel, NodeModel, EdgeModel

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="function")
async def db_session():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    
    async with async_session() as session:
        yield session
        await session.rollback()
    
    await engine.dispose()

@pytest.fixture
def client(db_session):
    def override_get_db():
        return db_session
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]

@pytest.fixture
async def test_graph(db_session):
    graph = GraphModel()
    db_session.add(graph)
    await db_session.flush()
    
    nodes = [
        NodeModel(name="A", graph_id=graph.id),
        NodeModel(name="B", graph_id=graph.id),
        NodeModel(name="C", graph_id=graph.id)
    ]
    db_session.add_all(nodes)
    await db_session.flush()
    
    edges = [
        EdgeModel(source_id=nodes[0].id, target_id=nodes[1].id, graph_id=graph.id),
        EdgeModel(source_id=nodes[1].id, target_id=nodes[2].id, graph_id=graph.id)
    ]
    db_session.add_all(edges)
    await db_session.commit()
    
    return graph.id