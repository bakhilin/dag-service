from pydantic import BaseModel, Field, field_validator
from typing import List

class NodeBase(BaseModel):
    """Node"""
    name: str = Field(..., max_length=255, pattern="^[a-zA-Z]+$",
                     description="Latin alphabet",
                )

class EdgeBase(BaseModel):
    """Edge"""
    source: str = Field(..., description="Sender Node")
    target: str = Field(..., description="Receiver Node")

class GraphCreate(BaseModel):
    """Graph model"""
    nodes: List[NodeBase] = Field(..., min_items=1, 
                                description="List Nodes of graph")
    edges: List[EdgeBase] = Field(..., description="List edges of graph")

    #@field_validator()

class GraphResponse(BaseModel):
    """Response object of graph"""
    id: int = Field(..., description="ID of graph")
    nodes: List[NodeBase] = Field(..., description="List of Nodes")
    edges: List[EdgeBase] = Field(..., description="List of Edges")

class AdjacencyListResponse(BaseModel):
    """List of adjacency"""
    adjacency_list: dict[str, List[str]] = Field(...,
        example={"a": ["b", "c"], "b": ["c"], "c": []},
        description="Key - nodes, values - neighbors"
    )