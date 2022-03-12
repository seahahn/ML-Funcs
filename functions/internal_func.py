import json

FUNCTIONS = {
    "sum"   : lambda x: x.sum,
    "count" : lambda x: x.count,
    "mean"  : lambda x: x.mean,
    "min"   : lambda x: x.min,
    "max"   : lambda x: x.max,
    "std"   : lambda x: x.std,
    "median": lambda x: x.median,
}


def boolean(x):
    if   x.lower() == "true" : return True
    elif x.lower() == "false": return False


def isint(x:str) -> bool:
    if type(x) == str:
        if x.isnumeric(): return True
        else            : return False
    elif type(x) == int:
        return True
    else:
        return False


import psycopg2

def save_log(query):
    # params = json.load(".env")
    # db = psycopg2.connect(
    #     **params
    # )
    # cursor = db.cursor()
    # insert_into = """INSERT INTO {schema}.{table}({column}) VALUES ('{data}')"""

    # cursor.execute(query)
    print(query)



from typing import Optional
from fastapi import Header
import datetime, inspect
def check_error(func):
    async def wrapper(*args, user_id: Optional[str] = Header(None), **kwargs):
        name = func.__name__
        start = datetime.datetime.now()
        try:
            tf, return_value = await func(*args, **kwargs)
            end = datetime.datetime.now()
            is_worked = 0 if tf else 1
            
            query = """INSERT INTO {}.{}({}) VALUES ("{}")"""
            save_log(query)
            return return_value
        except:
            end = datetime.datetime.now()
            # Unexpected error
            query = """비정상적인 동작"""
            is_worked = 2
            save_log(query)
            return "알 수 없는 에러 발생"
    
    ## FastAPI 에서 데코레이터를 사용할 수 있도록 파라미터 수정
    wrapper.__signature__ = inspect.Signature(
        parameters = [
            # Use all parameters from function
            *inspect.signature(func).parameters.values(),
            # Skip *args and **kwargs from wrapper parameters:
            *filter(
                lambda p: p.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD),
                inspect.signature(wrapper).parameters.values()
            ),
        ],
        return_annotation = inspect.signature(func).return_annotation,
    )

    return wrapper