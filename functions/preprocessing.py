from typing import Optional
from fastapi import Request, Query
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, OrdinalEncoder
# import modin.pandas as pd

async def set_feature_target_split(
    item : Request,
    cols : str
) -> str:
    ...
    df = pd.read_json(await item.json())

    dfcols = set(df.columns)
    try:    cols = [i.strip() for i in cols.split(",") if i.strip() != ""]
    except: return f"올바르지 않은 입력: {cols}"
    if not set(cols) <= dfcols: return f'"{cols}" is not in columns of DataFrame. It should be in {dfcols}'

    y = df[cols]
    X = df.drop(cols, axis=1)
    # how to return?
    # 1안 
    # return json.dumps( {
    #     "X": X.to_json(orient="records"),
    #     "y": y.to_json(orient="records"),
    # } )


async def set_train_test_split(
    item    : Request,
    col     : str,
    *,
    cols    : Optional[str] = Query(None, max_length=50), # for func
    col_from: Optional[str] = Query(None, max_length=50), # for func
    col_to  : Optional[str] = Query(None, max_length=50), # for func
    func    : Optional[str] = Query(None, max_length=50),
    cols_ops: Optional[str] = Query(None, max_length=50),
) -> str:

    # X_train, X_test, y_train, y_test = train_test_split(
    #     X, y
    #     test_size=None,
    #     train_size=None,
    #     random_state=None,
    #     shuffle=True,
    #     stratify=None,
    # )
    # 시계열 기준일 경우 
    # shuffle  = False,
    # stratify = None

    # how to return?
    # 1안 
    # return json.dumps( {
    #     "X_train": X_train.to_json(orient="records"),
    #     "X_test" : X_test.to_json(orient="records"),
    #     "y_train": y_train.to_json(orient="records"),
    #     "y_test" : y_test.to_json(orient="records"),
    # } )
    ...


async def set_one_hot_encoder():
    ...


async def set_target_encoder():
    ...


async def set_ordinal_encoder():
    ...

