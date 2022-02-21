from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000" # 포트 지정 안 하면 CORS 에러 발생
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    get_col_condition,
    get_loc,
    get_iloc,

    set_transpose,
    set_groupby,
    set_drop,
    set_dropna,
    set_rename,
    set_sort_values,
    set_merge,
    set_concat
)

create_upload_file = app.post("/uploadfile")          (create_upload_file)
get_head           = app.post("/file/head")           (get_head)
get_tail           = app.post("/file/tail")           (get_tail)
get_shape          = app.post("/file/shape")          (get_shape)
get_dtype          = app.post("/file/dtype")          (get_dtype)
get_columns        = app.post("/file/columns")        (get_columns)
get_unique         = app.post("/file/unique")         (get_unique)
get_unique_column  = app.post("/file/unique/{column}")(get_unique_column)
get_na             = app.post("/file/isna")           (get_na)
get_corr           = app.post("/file/corr")           (get_corr)
get_describe       = app.post("/file/describe")       (get_describe)
get_col_condition  = app.post("/file/{col}/condition")(get_col_condition)
get_loc            = app.post("/file/loc")            (get_loc)
get_iloc           = app.post("/file/iloc")           (get_iloc)

set_transpose      = app.post("/file/transpose")      (set_transpose)
set_groupby        = app.post("/file/groupby/{func}") (set_groupby)
set_drop           = app.post("/file/drop")           (set_drop)
set_dropna         = app.post("/file/dropna")         (set_dropna)
set_rename         = app.post("/file/rename")         (set_rename)
set_sort_values    = app.post("/file/sort/values")    (set_sort_values)
# set_sort_index     = app.post("/file/sort/index")     (set_sort_index)
set_merge          = app.post("/file/merge")          (set_merge)
set_concat         = app.post("/file/concat")         (set_concat)