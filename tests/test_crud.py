import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.graph import GraphModel, NodeModel
from sqlalchemy import select
from src.crud.graph import CRUDOperation

@pytest.mark.asyncio
class TestCRUDOperations:
    async def test_create_graph_success(self, db_session: AsyncSession):
        crud_operation = CRUDOperation(db_session)
        
        nodes = [{"name": "A"}, {"name": "B"}]
        edges = [{"source": "A", "target": "B"}]
        
        graph = await crud_operation.create_graph( nodes=nodes, edges=edges)
        assert isinstance(graph, GraphModel)
        assert graph.id is not None

        result = await db_session.execute(select(NodeModel))
        db_nodes = result.scalars().all()
        assert len(db_nodes) == 2
        assert {n.name for n in db_nodes} == {"A", "B"}

    async def test_get_full_graph(self, db_session: AsyncSession, test_graph: int):
        crud_operation = CRUDOperation(db_session)
        graph_data = await crud_operation.get_full_graph(test_graph)
        assert graph_data["id"] == test_graph
        assert len(graph_data["nodes"]) == 3
        assert len(graph_data["edges"]) == 2

    async def test_get_full_graph_not_found(self, db_session: AsyncSession):
        crud_operation = CRUDOperation(db_session)
        with pytest.raises(ValueError, match="Graph entity not found"):
            await crud_operation.get_full_graph(999)

    async def test_get_graph(self, db_session: AsyncSession, test_graph: int):
        crud_operation = CRUDOperation(db_session)        
        graph = await crud_operation.get_graph(test_graph)
        assert isinstance(graph, GraphModel)
        assert graph.id == test_graph

    async def test_get_graph_not_found(self, db_session: AsyncSession):
        crud_operation = CRUDOperation(db_session)        
        graph = await crud_operation.get_graph(999)
        assert graph is None

    async def test_get_adjacency_list(self, db_session: AsyncSession, test_graph: int):
        crud_operation = CRUDOperation(db_session)
        adj_list = await crud_operation.get_adjacency_list( test_graph)
        assert adj_list == {
            "A": ["B"],
            "B": ["C"],
            "C": []
        }

    async def test_get_adjacency_list_not_found(self, db_session: AsyncSession):
        crud_operation = CRUDOperation(db_session)
        adj_list = await crud_operation.get_adjacency_list(999)
        assert adj_list is None

    async def test_get_reverse_adjacency_list(self, db_session: AsyncSession, test_graph: int):
        crud_operation = CRUDOperation(db_session)
        reverse_adj = await crud_operation.get_reverse_adjacency_list(test_graph)
        assert reverse_adj == {
            "A": [],
            "B": ["A"],
            "C": ["B"]
        }

    async def test_get_reverse_adjacency_list_not_found(self, db_session: AsyncSession):
        crud_operation = CRUDOperation(db_session)
        reverse_adj = await crud_operation.get_reverse_adjacency_list(999)
        assert reverse_adj is None

    async def test_delete_node_success(self, db_session: AsyncSession, test_graph: int):
        crud_operation = CRUDOperation(db_session)
        success = await crud_operation.delete_node( test_graph, "B")
        assert success is True

    async def test_delete_node_not_found(self, db_session: AsyncSession, test_graph: int):
        crud_operation = CRUDOperation(db_session)
        success = await crud_operation.delete_node(test_graph, "X")
        assert success is False

    async def test_is_dag_acyclic(self):
        nodes = ["A", "B", "C"]
        edges = [{"source": "A", "target": "B"}, {"source": "B", "target": "C"}]
        assert await CRUDOperation.is_dag(nodes, edges) is True

    async def test_is_dag_cyclic(self):
        nodes = ["A", "B", "C"]
        edges = [
            {"source": "A", "target": "B"},
            {"source": "B", "target": "C"},
            {"source": "C", "target": "A"}
        ]
        assert await CRUDOperation.is_dag(nodes, edges) is False