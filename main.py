from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000", # 포트 지정 안 하면 CORS 에러 발생
    "https://front-web-xi.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from functions import (
    create_upload_file,

    head,
    tail,
    shape,
    dtype,
    columns,
    unique,
    # get_unique_column,
    isna,
    corr,
    describe,
    col_condition,
    loc,
    iloc,

    transpose,
    groupby,
    drop,
    dropna,
    rename,
    sort_values,
    merge,
    concat,
    set_column,
    astype,

    feature_target_split,
    train_test_split,
)

from visualization import (
    box_plot,
    hist_plot,
    count_plot,
    scatter_plot
    )

create_upload_file = app.post("/uploadfile")               (create_upload_file)
head               = app.post("/dataframe/head")           (head)
tail               = app.post("/dataframe/tail")           (tail)
shape              = app.post("/dataframe/shape")          (shape)
dtype              = app.post("/dataframe/dtype")          (dtype)
columns            = app.post("/dataframe/columns")        (columns)
unique             = app.post("/dataframe/unique")         (unique)
# get_unique_column  = app.post("/dataframe/unique/{column}")(get_unique_column)
isna               = app.post("/dataframe/isna")           (isna)
corr               = app.post("/dataframe/corr")           (corr)
describe           = app.post("/dataframe/describe")       (describe)
col_condition      = app.post("/dataframe/col_condition")  (col_condition)
loc                = app.post("/dataframe/loc")            (loc)
iloc               = app.post("/dataframe/iloc")           (iloc)

transpose          = app.post("/dataframe/transpose")      (transpose)
groupby            = app.post("/dataframe/groupby")        (groupby)
drop               = app.post("/dataframe/drop")           (drop)
dropna             = app.post("/dataframe/dropna")         (dropna)
rename             = app.post("/dataframe/rename")         (rename)
sort_values        = app.post("/dataframe/sort_values")    (sort_values)
# set_sort_index     = app.post("/dataframe/sort/index")     (set_sort_index)
merge              = app.post("/dataframe/merge")          (merge)
concat             = app.post("/dataframe/concat")         (concat)
set_column         = app.post("/dataframe/set_column")     (set_column)
astype             = app.post("/dataframe/astype")         (astype)

feature_target_split = app.post("/dataframe/feature_target_split")(feature_target_split)
train_test_split     = app.post("/dataframe/train_test_split")    (train_test_split)


box_plot     = app.post("/plot/boxplot")(box_plot)
hist_plot    = app.post("/plot/histplot")(hist_plot)
count_plot   = app.post("/plot/countplot")(count_plot)
scatter_plot = app.post("/plot/scatterplot")(scatter_plot)


