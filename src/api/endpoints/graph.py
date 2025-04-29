from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.models.graph import GraphModel, EdgeModel
from src.crud.graph import CRUDOperation
from src.db.session import get_db

from src.schemas.graph import (
    GraphCreate,
    GraphResponse,
    AdjacencyListResponse
)

class ENDPoints:
    def __init__(self):
        self.router = APIRouter()
        self._init_routes()

    def _init_routes(self):
        self.router.post("/", response_model=GraphResponse, status_code=status.HTTP_201_CREATED)(self.create_graph_api_graph__post)
        self.router.get("/{graph_id}/", response_model=GraphResponse)(self.read_graph_api_graph__graph_id___get)
        self.router.get("/{graph_id}/adjacency_list", response_model=AdjacencyListResponse)(self.get_adjacency_list_api_graph__graph_id__adjacency_list_get)
        self.router.get("/{graph_id}/reverse_adjacency_list")(self.get_reverse_adjacency_list_api_graph__graph_id__reverse_adjacency_list_get)
        self.router.delete("/{graph_id}/node/{node_name}", status_code=status.HTTP_204_NO_CONTENT)(self.delete_node_api_graph__graph_id__node__node_name__delete)

    async def create_graph_api_graph__post(
        self,
        graph: GraphCreate,
        db: AsyncSession = Depends(get_db)
    ):
        """Ручка для создания графа, принимает граф в виде списка вершин и списка ребер."""
        crud_operations = CRUDOperation(db)
        try:
            db_graph = await crud_operations.create_graph(
                nodes=[{"name": node.name} for node in graph.nodes],
                edges=[{"source": edge.source, "target": edge.target} for edge in graph.edges]
            )
            
            result = await db.execute(
                select(GraphModel)
                .where(GraphModel.id == db_graph.id)
                .options(
                    selectinload(GraphModel.nodes),
                    selectinload(GraphModel.edges)
                    .selectinload(EdgeModel.source),
                    selectinload(GraphModel.edges)
                    .selectinload(EdgeModel.target)
                )
            )
            db_graph = result.scalars().first()
            
            return {
                "id": db_graph.id,
                "nodes": [{"name": node.name} for node in db_graph.nodes],
                "edges": [{
                    "source": edge.source.name,
                    "target": edge.target.name
                } for edge in db_graph.edges]
            }
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": "Failed to add graph"}
            )

    async def read_graph_api_graph__graph_id___get(
        self,
        graph_id: int,
        db: AsyncSession = Depends(get_db)
    ):
        """Ручка для чтения графа в виде списка вершин и списка ребер."""
        crud_operations = CRUDOperation(db)
        try:
            graph_data = await crud_operations.get_full_graph(graph_id) 
            return graph_data
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": "Graph entity not found"}
            )

    async def get_adjacency_list_api_graph__graph_id__adjacency_list_get(
        self,
        graph_id: int,
        db: AsyncSession = Depends(get_db)
    ):
        """Ручка для чтения графа в виде списка смежности.\nСписок смежности представлен в виде пар ключ - значение, где\n- ключ - имя вершины графа,\n- значение - список имен всех смежных вершин (всех потомков ключа)."""
        crud_operations = CRUDOperation(db)
        adjacency = await crud_operations.get_adjacency_list( graph_id)
        if not adjacency:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": f"Graph entity not found"}
            )
        return {"adjacency_list": adjacency}

    async def get_reverse_adjacency_list_api_graph__graph_id__reverse_adjacency_list_get(
        self,
        graph_id: int,
        db: AsyncSession = Depends(get_db)
    ):
        """Ручка для чтения транспонированного графа в виде списка смежности.\nСписок смежности представлен в виде пар ключ - значение, где\n- ключ - имя вершины графа,\n- значение - список имен всех смежных вершин (всех предков ключа в исходном графе)."""
        crud_operations = CRUDOperation(db)
        reverse_adjacency = await crud_operations.get_reverse_adjacency_list(graph_id)
        if not reverse_adjacency:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": f"Graph entity not found"}
            )
        return {"adjacency_list": reverse_adjacency}


    async def delete_node_api_graph__graph_id__node__node_name__delete(
        self,
        graph_id: int,
        node_name: str,
        db: AsyncSession = Depends(get_db)
    ):
        """Ручка для удаления вершины из графа по ее имени."""
        crud_operations = CRUDOperation(db)
        success = await crud_operations.delete_node(graph_id, node_name)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": f"Graph entity not found"}
            )