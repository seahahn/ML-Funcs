from typing import Optional
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Request):
    return {"item": item, "item_id": item_id}


from functions import create_upload_file

create_upload_file = app.post("/uploadfile/")(create_upload_file)
