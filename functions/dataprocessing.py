from typing import Optional
from fastapi import Request, Query
import numpy as np
import pandas as pd
# import modin.pandas as pd


async def read_head(item:Request, line: Optional[str] = Query(5, max_length=50)) -> dict:
    try:    line = int(line)
    except: line = 5
    return pd.read_json(await item.json()).head(line).to_dict()

async def read_tail(item:Request, line: Optional[str] = Query(5, max_length=50)) -> dict:
    try:    line = int(line)
    except: line = 5
    return pd.read_json(await item.json()).tail(int(line)).to_dict()

async def read_shape(item:Request) -> dict:
    return pd.read_json(await item.json()).shape

async def read_dtype(item:Request) -> dict:    
    return {i:str(v) for i,v in pd.read_json(await item.json()).dtypes.to_dict().items()}

async def read_describe(
    item:                Request,
    *,
    per25:               Optional[str] = Query(.25, max_length=50),
    per50:               Optional[str] = Query(.50, max_length=50),
    per75:               Optional[str] = Query(.75, max_length=50),
    num:                 Optional[str] = Query(0,   max_length=50),
    obj:                 Optional[str] = Query(0,   max_length=50),
    cat:                 Optional[str] = Query(0,   max_length=50),
    datetime_is_numeric: Optional[str] = Query("",  max_length=50)
    ) -> dict:

    try:    per25 = float(per25)
    except: per25 = .25
    try:    per50 = float(per50)
    except: per50 = .50
    try:    per75 = float(per75)
    except: per75 = .75

    """
    Pandas data type
    "int"       # np.number
    "float"     # np.number
    "object"    # np.object, "O"
    "category"  # "category"
    
    Not use
    "datetime"  #
    "timedelta" #
    "bool"      # 
    """
    include = []
    exclude = []
    if num:
        if int(num) > 0: include.append(np.number)
        else           : exclude.append(np.number)
    if obj:
        if int(obj) > 0: include.append(object)
        else           : exclude.append(object)
    if cat:
        if int(cat) > 0: include.append("category")
        else           : exclude.append("category")

    return pd.read_json(await item.json()).describe(
        percentiles         = [ float(per25), float(per50), float(per75) ],
        include             = include if include else None,
        exclude             = exclude if exclude else None,
        datetime_is_numeric = True if datetime_is_numeric.lower() == "true" else False
    ).to_json()
