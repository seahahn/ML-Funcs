from typing import Optional
from fastapi import Request, Query
import json
import numpy as np
import pandas as pd
# import modin.pandas as pd


async def get_head(item: Request, *, line: Optional[str] = Query(5, max_length=50)) -> str:
    try:    line = int(line)
    except: line = 5
    return pd.read_json(await item.json()).head(line).to_json()


async def get_tail(item: Request, *, line: Optional[str] = Query(5, max_length=50)) -> str:
    try:    line = int(line)
    except: line = 5
    return pd.read_json(await item.json()).tail(int(line)).to_json()


async def get_shape(item: Request) -> str:
    return json.dumps(pd.read_json(await item.json()).shape)


async def get_dtype(item: Request) -> str:    
    return json.dumps({i:str(v) for i,v in pd.read_json(await item.json()).dtypes.to_dict().items()})


async def get_columns(item: Request) -> str:
    return f"{list(pd.read_json(await item.json()).columns)}"


async def get_unique(item: Request) -> str:
    """입력이 Series의 JSON일 경우"""
    try:
        return f"{list(pd.read_json(await item.json()).unique())}"
    except:
        return "input JSON should be converted to pandas.Series"


async def get_unique_column(column: str, item: Request) -> str:
    """입력이 DataFrame의 JSON일 경우

    /file/unique/컬럼명 에서 컬럼명이 DataFrame에 없을 경우 에러메시지를 리턴한다."""
    df = pd.read_json(await item.json())
    try:
        if column not in df.columns:
            return f"{column} is not in columns of DataFrame. It should be in {list(df.columns)}"
        return f"{list(df[column].unique())}"
    except:
        return "input JSON should be converted to pandas.DataFrame"


async def get_na(item: Request, *, sum: Optional[str] = Query("false", max_length=50)) -> str:
    """결측치 확인 함수
    `/file/isna`
    `/file/isna?sum=true`

    Args:
    ```
    item (Request) : JSON, 사용할 때 `await item.json()`
    sum  (optional): default = "false"
                     "true" 일 경우 결측치의 합을 포함한 시리즈를 리턴
    ```
    Returns:
    ```
    (str): JSON
    ```
    """
    if   sum.lower() == "true" : return pd.read_json(await item.json()).isna().sum().to_json()
    elif sum.lower() == "false": return pd.read_json(await item.json()).isna().to_json()
    else                       : return "sum은 true or false를 넣으셔야 합니다."


async def get_corr(
    item   : Request,
    *,
    method : Optional[str] = Query("pearson", max_length=50),
    req_min: Optional[str] = Query(1, max_length=50),
    col1   : Optional[str] = Query(None, max_length=50),
    col2   : Optional[str] = Query(None, max_length=50),
) -> str:
    """상관관계를 반환해주는 함수
    ```
    req_min은 상관관계를 구하기 위해 필요한 최소한의 데이터 수를 의미합니다.
    만약 na 값이 많아서 유의미한 데이터를 구하기 어려운 경우 req_min을 통해 해당 columns에서 구한 상관관계 값을 NaN으로 바꿀 수 있습니다.

    col1, col2는 데이터가 클 때, 보고 싶은 데이터만 볼수 있는 기능입니다.
    col1, col2 둘 다 입력: 두 columns의 상관관계만 리턴
    col1, col2 둘 중 하나: 해당 column과 나머지의 상관관계를 리턴
    ```
    Args:
    ```
    item   (Request, required): JSON
    method     (str, optional): Default "pearson", 상관관계 방식. 셋 중 하나 ["pearson", "kendall", "spearman"]
    req_min    (str, optional): Default 1,         상관관계 계산에 필요한 최소 데이터 수. 양의 정수
    col1       (str, optional): Default None,      columns명, DataFrame에 없으면 에러 반환
    col2       (str, optional): Default None,      columns명, DataFrame에 없으면 에러 반환
    ```
    Returns:
    ```
    (str): JSON
    ```
    """
    if not method in ["pearson", "kendall", "spearman"]:
        return 'method should be in ["pearson", "kendall", "spearman"]'
    
    try   : 
        req_min = int(req_min)
        if req_min <= 0:
            raise Exception
    except: 
        return "req_min should be positive integer"
    
    df = pd.read_json(await item.json())
    cols = list(df.columns)
    if col1 and col1 not in cols:
        return f"{col1} is not in columns of DataFrame. It should be in {cols}"
    if col2 and col2 not in cols:
        return f"{col2} is not in columns of DataFrame. It should be in {cols}"
    
    if col1 and col2:
        return json.dumps(df[col1].corr(
            other       = df[col2],
            method      = method, 
            min_periods = req_min
        ))
    elif col1:
        return df.corr(
            method      = method, 
            min_periods = req_min
        )[col1].to_json()
    elif col2:
        return df.corr(
            method      = method, 
            min_periods = req_min
        )[col2].to_json()
    else:
        return df.corr(
            method      = method, 
            min_periods = req_min
        ).to_json()


async def get_describe(
    item:        Request,
    *,
    percentiles: Optional[str] = Query(None, max_length=50),
    num:         Optional[str] = Query(0,    max_length=50),
    obj:         Optional[str] = Query(0,    max_length=50),
    cat:         Optional[str] = Query(0,    max_length=50),
    date:        Optional[str] = Query(0,    max_length=50),
    date2num:    Optional[str] = Query("",   max_length=50)
) -> str:
    """pandas.DataFrame.describe() 결과를 리턴하는 함수
    ```
    percentiles는 보고 싶은 퍼센트의 값을 볼 수 있는 파라미터입니다.
    default로 min, 25%, 50%, 75%, max의 데이터를 반환하는데, 이 옵션을 주면
    다른 min, 50%, max에 추가로 다른 퍼센트의 데이터를 볼 수 있습니다.

    입력은 소수(float)의 배열인데, 쉽표로 구분해주시면 됩니다. 
    ex) min, 10%, 30%, 50% 70% max를 보려면 => .1,.3,.7

    num, obj, cat, date는 해당 자료형을 볼지 안 볼지 결정하는 파라미터입니다.
    default는 0으로 조작을 하지 않는 것입니다.
    넷 전부 0일 경우 default로 numeric 데이터만 보여줍니다.

    1 :해당 자료형의 describe(넷 중 1인 데이터만 보여줍니다.)
    -1:해당 자료형을 제외한 나머지의 describe(넷 중 -1이 아닌 데이터만 보여줍니다.)

    date2num은 true일 경우 datetime 자료형을 numeric 자료형으로 바꿔줍니다.
    ```
    Args:
    ```
    item       (Request, required): JSON
    percentiles(str,     optional): Default None, 해당 퍼센트의 데이터 값을 확인, 쉼표로 구분한 float array: ex) 0.1,0.2,0.4,0.8
    num        (str,     optional): Default 0,    numeric 데이터, -1, 0, 1 중 하나
    obj        (str,     optional): Default 0,    object 데이터, -1, 0, 1 중 하나
    cat        (str,     optional): Default 0,    category 데이터, -1, 0, 1 중 하나
    date       (str,     optional): Default 0,    datetime 데이터, -1, 0, 1 중 하나
    date2num   (str,     optional): Default "",   datetime 데이터를 numeric 데이터로 변환, ture(대소구분X)만 바뀜.
    ```
    Returns:
    ```
    (str): JSON
    ```
    """


    try:    percentiles = list(map(float,percentiles.split(","))) if percentiles else None
    except: return json.dumps("percentiles should be 0~1 float string divided by ','")
    try:    num = int(num)
    except: return json.dumps("num should be -1, 0, 1")
    try:    obj = int(obj)
    except: return json.dumps("obj should be -1, 0, 1")
    try:    cat = int(cat)
    except: return json.dumps("cat should be -1, 0, 1")
    try:    date = int(date)
    except: return json.dumps("date should be -1, 0, 1")
    """
    Pandas data type
    "int64"      # np.number
    "float64"    # np.number
    "object"     # object, "O"
    "category"   # "category"
    "datetime64" # np.datetime64
    
    Not use
    "timedelta"  #
    "bool"       # 
    """

    df = pd.read_json(await item.json())
    chk = {str(i) for i in df.dtypes.unique()}
    
    include = []
    exclude = []

    if num:
        if num > 0 : include.append(np.number)     if "int64" in chk or "float64" in chk else ...
        else       : exclude.append(np.number)
    if obj:
        if obj > 0 : include.append(object)        if "object" in chk else ...
        else       : exclude.append(object)
    if cat:
        if cat > 0 : include.append("category")    if "category" in chk else ...
        else       : exclude.append("category")
    if date:
        if date > 0: include.append(np.datetime64) if "datetime64[ns]" in chk else ...
        else       : exclude.append(np.datetime64)
    if len(include) == 3:
        include = "all"
    if len(exclude) == 3:
        exclude = None

    return df.describe(
        percentiles         = percentiles,
        include             = include if include else None,
        exclude             = exclude if exclude else None,
        datetime_is_numeric = True if date2num.lower() == "true" else False
    ).to_json()
