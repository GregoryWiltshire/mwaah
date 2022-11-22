from typing import List

from pydantic import BaseModel


class Dag(BaseModel):
    dag_id: str
    filepath: str
    owner: str
    paused: bool


class DagList(BaseModel):
    __root__: List[Dag]

