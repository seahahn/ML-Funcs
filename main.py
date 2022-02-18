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


from functions import (
    create_upload_file, 
    read_head, 
    read_tail, 
    read_shape,
    read_dtype,
    read_describe
)

create_upload_file = app.post("/uploadfile")   (create_upload_file)
read_head          = app.post("/file/head")    (read_head)
read_tail          = app.post("/file/tail")    (read_tail)
read_shape         = app.post("/file/shape")   (read_shape)
read_dtype         = app.post("/file/dtype")   (read_dtype)
read_describe      = app.post("/file/describe")(read_describe)