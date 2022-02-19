from typing import Optional
from fastapi import Request, Query
import json
import numpy as np
import pandas as pd

async def set_transpose(item: Request) -> str:
    return pd.read_json(await item.json()).transpose().to_json()


async def set_groupby(
    func:       str,
    item:       Request,
    by:         str,
    *,
    axis:       Optional[str] = Query(0,     max_length=50),
    # level:      Optional[str] = Query(None,  max_length=50), # MultiIndex 에서 사용하는 것! 
    as_index:   Optional[str] = Query("True",  max_length=50), 
    sort:       Optional[str] = Query("True",  max_length=50), 
    group_keys: Optional[str] = Query("True",  max_length=50), 
    observed:   Optional[str] = Query("False", max_length=50), 
    dropna:     Optional[str] = Query("True",  max_length=50)
) -> str:
    """pandas.DataFrame.groupby(by).func() 결과를 리턴하는 함수
    ```
    available function = sum, count, mean, min, max, std, median, size
    by는 반드시 존재하는 컬럼명을 쉼표로 구분해서 입력해야 한다. 1개만 입력할 경우 쉽표 X
    axis = 0(row), 1(columns)
    as_index, sort, group_keys, observed, dropna = bool. true나 false가 입력되어야 한다.

    ※ 추후 level 기능 구현 예정
    ```
    Args:
    ```
    func       (str,     required): should be in [sum, count, mean, min, max, std, median, size]
    item       (Request, required): JSON
    by         (str,     required): should be string array(column names) divied by ","
    *
    axis       (str,     optional): Default: 0,      0(row), 1(columns)
    as_index   (str,     optional): Default: "True"  ?
    sort       (str,     optional): Default: "True"  ?
    group_keys (str,     optional): Default: "True"  ?
    observed   (str,     optional): Default: "False" ?
    dropna     (str,     optional): Default: "True"  true면 na를 드랍, false면 na를 살려둠
    ```
    Returns:
    ```
    str: JSON
    ```
    """

    ## func
    func_list = ["sum", "count", "mean", "min", "max", "std", "median", "size"]
    if not func in func_list:
        return f'"{func}" is invalid function. "func" should be in {func_list}'
    
    df = pd.read_json(await item.json())

    ## by
    try:
        # if by is None:
        #     return '"by" is a required parameter.'
        by = by.split(",")
        error_list = [i for i in by if i not in df.columns]
        if error_list:
            return f'"by" should be string array(column names) divied by ","\nlist not in DataFrame columns: {error_list}'
    except:
        return '"by" should be string array(column names) divied by ","'

    ## axis
    try:
        axis = int(axis)
        if axis not in [0, 1]: return '"axis" should be 0, 1. row(0), column(1)'
    except:
        return '"axis" should be 0, 1. row(0), column(1)'
    
    ## level(미구현)
    # If the axis is a MultiIndex (hierarchical), group by a particular level or levels.

    ## as_index
    try:
        if   as_index.lower() == "true" : as_index = True
        elif as_index.lower() == "false": as_index = False
    except:
        return '"as_index" should be bool, "true" or "false"'

    ## sort
    try:
        if   sort.lower() == "true" : sort = True
        elif sort.lower() == "false": sort = False
    except:
        return '"sort" should be bool, "true" or "false"'
    
    ## group_keys
    try:
        if   group_keys.lower() == "true" : group_keys = True
        elif group_keys.lower() == "false": group_keys = False
    except:
        return '"group_keys" should be bool, "true" or "false"'

    ## squeeze(미구현)
    # squeeze will deprecated in future version

    ## observed
    try:
        if   observed.lower() == "true" : observed = True
        elif observed.lower() == "false": observed = False
    except:
        return '"observed" should be bool, "true" or "false"'

    ## dropna
    try:
        if   dropna.lower() == "true" : dropna = True
        elif dropna.lower() == "false": dropna = False
    except:
        return '"dropna" should be bool, "true" or "false"'


    # pd.DataFrame.groupby
    df_group = df.groupby(
        by         = by,
        axis       = axis,
        # level      = level,
        as_index   = as_index,
        sort       = sort,
        group_keys = group_keys,
        observed   = observed,
        dropna     = dropna
    )
    df_group
    functions = {
        "sum"   : df_group.sum,
        "count" : df_group.count,
        "mean"  : df_group.mean,
        "min"   : df_group.min,
        "max"   : df_group.max,
        "std"   : df_group.std,
        "median": df_group.median,
        "size"  : df_group.size
    }
    print(functions[func]())
    return functions[func]().to_json()


async def set_drop(
    item:    Request, 
    labels:  str,
    *,
    axis:    Optional[str] = Query(0,       max_length=50),
    errors:  Optional[str] = Query("raise", max_length=50),
    # index:   Optional[str] = Query(None,    max_length=50), if axis = 0 : index = labels
    # columns: Optional[str] = Query(None,    max_length=50), elif axis = 1 : columns = labels
    # level:   Optional[str] = Query(None,    max_length=50), # level is for multi-index
    # inplace: Optional[str] = Query(False,   max_length=50), # inplace is not need this way
) -> str:
    """pandas.DataFrame.drop(labels) 를 리턴하는 함수
    ```
    labels는 반드시 존재하는 컬럼 or 인덱스명을 쉼표로 구분해서 입력해야 한다. 1개만 입력할 경우 쉽표 X
    axis = 0(row), 1(columns)
    ```
    Args:
    ```
    item   (Request, required): JSON
    labels (str,     required): should be string/int array(index or column names) divied by ","
    *
    axis   (str,     optional): Default: 0,      0(row, index), 1(columns)
    errors (str,     optional): Default: "raise" raise면 없는 것을 drop 시도할 때 에러 발생, ignore면 에러 발생X
    ```
    Returns:
    ```
    str: JSON
    ```
    """
    ## errors
    if errors not in ["raise", "ignore"]:
        return f'"errors" should be "raise" or "ignore". errors = {errors}'

    df = pd.read_json(await item.json())

    ## axis
    try:
        axis = int(axis)
        if axis not in [0, 1]: return '"axis" should be 0, 1. row(0), column(1)'
    except:
        return '"axis" should be 0, 1. row(0), column(1)'
    
    #labels
    try:
        # if labels is None:
        #     return '"labels" is a required parameter.'
        labels = labels.split(",")
        if errors == "raise":
            if axis: 
                cols = df.columns
                if str(cols.dtype) != "object": labels = [int(i) for i in labels]
                cols = set(cols)
                error_list = [i for i in labels if i not in cols]
            else:
                idxs = df.index
                if str(idxs.dtype) != "object": labels = [int(i) for i in labels]
                idxs = set(idxs)
                error_list = [i for i in labels if i not in idxs]
            if error_list:
                if axis: return f'"labels" should be string array(column names) divied by ","\nlist not in DataFrame columns: {error_list}'
                else   : return f'"labels" should be string array(index names) divied by ","\nlist not in DataFrame indexes: {error_list}'
    except:
        return '"labels" should be string array(column names) divied by ","'
    
    print(df.drop(labels, axis, errors = errors))
    return df.drop(
        labels = labels,
        axis   = axis,
        errors = errors,
        # index=None,
        # columns=None,
        # level=None,
        # inplace=False,
    ).to_json()
