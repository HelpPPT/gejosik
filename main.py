from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from gejosik import Gejosik

app = FastAPI()

g = Gejosik()

class Item(BaseModel):
    vocabulary: str | None = None

@app.post("/items/")
def parse_item(item: Item):
    t = g.sentence(item.vocabulary)
    return t