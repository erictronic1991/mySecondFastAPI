from fastapi import FastAPI
from pydantic import BaseModel

class Todo_ModelFormat(BaseModel):
    id: int
    item: str