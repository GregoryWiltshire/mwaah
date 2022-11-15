from pydantic import BaseModel
from typing import List

class Dag(BaseModel):
    dag_id: str
    filepath: str
    owner: str
    paused: bool

class DagList(BaseModel):
     __root__: List[Dag]

