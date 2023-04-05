from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from gejosik import Gejosik

app = FastAPI()
g = Gejosik()

class Item(BaseModel):
    sentence: str | None = None

@app.post("/gejosik/")
def parse_item(item: Item):
    t = g.sentence(item.sentence)
    return t