from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base import Base

class GraphModel(Base):
    __tablename__ = "graphs"

    id = Column(Integer, primary_key=True, index=True)
    nodes = relationship("NodeModel", back_populates="graph")
    edges = relationship("EdgeModel", back_populates="graph")

class NodeModel(Base):
    __tablename__ = "nodes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    graph_id = Column(Integer, ForeignKey("graphs.id"), nullable=False)
    
    source_edges = relationship("EdgeModel", foreign_keys="EdgeModel.source_id", back_populates="source")
    target_edges = relationship("EdgeModel", foreign_keys="EdgeModel.target_id", back_populates="target")
    graph = relationship("GraphModel", back_populates="nodes")

class EdgeModel(Base):
    __tablename__ = "edges"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("nodes.id"), nullable=False)
    target_id = Column(Integer, ForeignKey("nodes.id"), nullable=False)
    graph_id = Column(Integer, ForeignKey("graphs.id"), nullable=False)
    
    source = relationship("NodeModel", foreign_keys=[source_id], back_populates="source_edges")
    target = relationship("NodeModel", foreign_keys=[target_id], back_populates="target_edges")
    graph = relationship("GraphModel", back_populates="edges")