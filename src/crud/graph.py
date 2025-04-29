from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import Dict, List, Optional
from src.models.graph import GraphModel, NodeModel, EdgeModel
from sqlalchemy.orm import selectinload
    
class CRUDOperation:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_full_graph(self, graph_id: int) -> Dict:
        """Get info about graph"""
        result = await self.db.execute(
            select(GraphModel)
            .where(GraphModel.id == graph_id)
            .options(
                selectinload(GraphModel.nodes),
                selectinload(GraphModel.edges)
                .selectinload(EdgeModel.source),
                selectinload(GraphModel.edges)
                .selectinload(EdgeModel.target)
            )
        )
        graph = result.scalars().first()
        
        if not graph:
            raise ValueError("Graph entity not found")
        
        return {
            "id": graph.id,
            "nodes": [{"name": node.name} for node in graph.nodes],
            "edges": [{"source": edge.source.name, "target": edge.target.name} 
                    for edge in graph.edges]
        }

    async def get_all_graphs(self):
        result = await self.db.execute(select(GraphModel).options(
                selectinload(GraphModel.nodes),
                selectinload(GraphModel.edges)
                .selectinload(EdgeModel.source),
                selectinload(GraphModel.edges)
                .selectinload(EdgeModel.target)
            ))
        
        if result is None:
            raise ValueError("Graph entity not found")

        graphs = result.scalars().all()

        return [
            {
                "id": graph.id,
                "nodes": [{"name": node.name} for node in graph.nodes],
                "edges": [
                    {"source": edge.source.name, "target": edge.target.name}
                    for edge in graph.edges
                ]
            }
            for graph in graphs
        ]

    @staticmethod
    async def is_dag(nodes: List[str], edges: List[Dict[str, str]]) -> bool:
        """алгоритм Кана"""
        graph = {node: [] for node in nodes}
        in_degree = {node: 0 for node in nodes}
        
        try:
            for edge in edges:
                graph[edge["source"]].append(edge["target"])
                in_degree[edge["target"]] += 1
        except:
            raise ValueError("Failed to add graph")
        
        queue = [node for node in in_degree if in_degree[node] == 0]
        topo_order = []
        
        while queue:
            node = queue.pop()
            topo_order.append(node)
            
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        return len(topo_order) == len(nodes)

    async def create_graph(
        self,
        nodes: List[Dict],
        edges: List[Dict]
    ) -> GraphModel:  
        """Create new graph"""
        if not await self.is_dag([n["name"] for n in nodes], edges):
            raise ValueError("Failed to add graph. Must be asyclic!!!")
        
        async with self.db.begin():
            graph = GraphModel()
            self.db.add(graph)
            await self.db.flush()
            
            node_map = {}
            for node in nodes:
                db_node = NodeModel(name=node["name"], graph_id=graph.id)
                self.db.add(db_node)
                await self.db.flush()
                node_map[node["name"]] = db_node.id
            
            for edge in edges:
                db_edge = EdgeModel(
                    source_id=node_map[edge["source"]],
                    target_id=node_map[edge["target"]],
                    graph_id=graph.id
                )
                self.db.add(db_edge)
            
            await self.db.commit()
        
        return graph

    async def get_graph(self, graph_id: int) -> Optional[GraphModel]:
        """Get graph by ID"""
        result = await self.db.execute(
            select(GraphModel).where(GraphModel.id == graph_id)
        )
        return result.scalars().first()

    async def get_adjacency_list(self, graph_id: int) -> Optional[Dict[str, List[str]]]:
        """Get info about adjacency"""
        graph = await self.get_graph(graph_id)
        if not graph:
            return None
        
        result = await self.db.execute(
            select(NodeModel)
            .where(NodeModel.graph_id == graph_id)
            .options(selectinload(NodeModel.source_edges))
        )
        nodes = result.scalars().all()
        
        return {
            node.name: [edge.target.name for edge in node.source_edges]
            for node in nodes
        }

    async def get_reverse_adjacency_list(self, graph_id: int) -> Optional[Dict[str, List[str]]]:
        """Get reverse adjacency list"""
        graph = await self.get_graph( graph_id)
        if not graph:
            return None
        
        result = await self.db.execute(
            select(NodeModel)
            .where(NodeModel.graph_id == graph_id)
            .options(selectinload(NodeModel.target_edges))
        )
        nodes = result.scalars().all()
        
        return {
            node.name: [edge.source.name for edge in node.target_edges]
            for node in nodes
        }

    

    async def delete_node(self, graph_id: int, node_name: str) -> bool:
        """Delete node from graph"""
        async with self.db.begin():
            result = await self.db.execute(
                select(NodeModel)
                .where(NodeModel.graph_id == graph_id)
                .where(NodeModel.name == node_name)
            )
            node = result.scalars().first()
            
            if not node:
                return False
            
            await self.db.execute(
                delete(EdgeModel)
                .where(
                    (EdgeModel.source_id == node.id) | 
                    (EdgeModel.target_id == node.id)
                )
            )
            
            await self.db.delete(node)
            await self.db.commit()
        
        return True