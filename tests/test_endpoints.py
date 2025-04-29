import pytest
from fastapi import status

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}

class TestGraphEndpoints:
    @pytest.mark.asyncio
    async def test_create_graph(self, client):
        payload = {
            "nodes": [{"name": "A"}, {"name": "B"}],
            "edges": [{"source": "A", "target": "B"}]
        }
        response = client.post("/api/graph/", json=payload)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "id" in data
        assert len(data["nodes"]) == 2
        assert len(data["edges"]) == 1

    @pytest.mark.asyncio
    async def test_create_graph_validation_error(self, client):
        payload = {"invalid": "data"}
        response = client.post("/api/graph/", json=payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_get_graph(self, client, test_graph):
        response = client.get(f"/api/graph/{test_graph}/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_graph
        assert len(data["nodes"]) == 3
        assert len(data["edges"]) == 2

    @pytest.mark.asyncio
    async def test_get_nonexistent_graph(self, client):
        response = client.get("/api/graph/999/")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Graph entity not found" in response.json()["detail"]["message"]

    @pytest.mark.asyncio
    async def test_get_adjacency_list(self, client, test_graph):
        response = client.get(f"/api/graph/{test_graph}/adjacency_list")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "adjacency_list": {
                "A": ["B"],
                "B": ["C"],
                "C": []
            }
        }

    @pytest.mark.asyncio
    async def test_get_reverse_adjacency_list(self, client, test_graph):
        response = client.get(f"/api/graph/{test_graph}/reverse_adjacency_list")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "adjacency_list": {
                "A": [],
                "B": ["A"],
                "C": ["B"]
            }
        }

    @pytest.mark.asyncio
    async def test_delete_nonexistent_node(self, client, test_graph):
        response = client.delete(f"/api/graph/{test_graph}/node/X")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Graph entity not found" in response.json()["detail"]["message"]


    @pytest.mark.asyncio
    async def test_invalid_graph_id_format(self, client):
        response = client.get("/api/graph/invalid_id/")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_empty_graph_creation(self, client):
        payload = {
            "nodes": [],
            "edges": []
        }
        response = client.post("/api/graph/", json=payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


    @pytest.mark.asyncio
    async def test_graph_with_disconnected_nodes(self, client):
        payload = {
            "nodes": [{"name": "A"}, {"name": "B"}],
            "edges": []
        }
        response = client.post("/api/graph/", json=payload)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert len(data["nodes"]) == 2
        assert len(data["edges"]) == 0
    