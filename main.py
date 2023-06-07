from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gejosik import Gejosik

app = FastAPI()
g = Gejosik()

class Item(BaseModel):
    sentences: List[str]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/gejosik/")
def gejosik(item: Item):
    parsed_sentence = {}
    for sentence in item.sentences:
        t = g.sentence(sentence)
        parsed_sentence[t['original_sentence']] = t
    return parsed_sentence