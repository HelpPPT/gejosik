from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gejosik import Gejosik

app = FastAPI()
g = Gejosik()

class Item(BaseModel):
    sentence: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/gejosik/")
def parse_item(item: Item):
    if item.sentence == '':
        return '한 개 이상의 문자가 있어야 합니다.'
    t = str(g.sentence(item.sentence))
    return t