from pydantic import BaseModel
from typing import List, Optional

class Graph(BaseModel):
    nodes: List[int]
    edges: List[List[int]]

class PathResult(BaseModel):
    path: List[int]
    total_distance: Optional[float]
