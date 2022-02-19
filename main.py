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
    get_head, 
    get_tail, 
    get_shape,
    get_dtype,
    get_columns,
    get_unique,
    get_unique_column,
    get_na,
    get_corr,
    get_describe,
    set_transpose
)

create_upload_file = app.post("/uploadfile")          (create_upload_file)
get_head          = app.post("/file/head")           (get_head)
get_tail          = app.post("/file/tail")           (get_tail)
get_shape         = app.post("/file/shape")          (get_shape)
get_dtype         = app.post("/file/dtype")          (get_dtype)
get_columns       = app.post("/file/columns")        (get_columns)
get_unique        = app.post("/file/unique")         (get_unique)
get_unique_column = app.post("/file/unique/{column}")(get_unique_column)
get_na            = app.post("/file/isna")           (get_na)
get_corr          = app.post("/file/corr")           (get_corr)
get_describe      = app.post("/file/describe")       (get_describe)