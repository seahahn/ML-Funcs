import os
from dotenv import load_dotenv
load_dotenv()

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
    db = psycopg2.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PW"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME")
    )
    cursor = db.cursor()
    cursor.execute(query)

    cursor.close()
    db.commit()
    db.close()

from typing import Optional
from fastapi import Header, Cookie
import datetime, inspect, traceback, jwt

SECRET_KEY=os.getenv("SECRET_KEY")

def check_error(func):
    async def wrapper(*args, user_id: Optional[str] = Header(None), token: Optional[str] = Header(None), **kwargs):
        try:
            # 토큰을 검증하여 유효한 토큰인지 확인
            # JWT 토큰 인증되지 않으면 기능 작동 X (정상적인 사용자가 아닌 것으로 간주)
            at = token
            jwt.decode(at, SECRET_KEY, algorithms="HS256")
        except Exception as e:
            return {"result":False, "token_state":False, "message":str(e)}

        name = func.__name__
        start = datetime.datetime.now(tz=datetime.timezone.utc)
        try:
            tf, return_value = await func(*args, **kwargs)
            end = datetime.datetime.now(tz=datetime.timezone.utc)
            is_worked = 0 if tf else 1

            query = f"""INSERT INTO
                public.func_log (user_idx, func_code, is_worked, start_time, end_time)
                VALUES ({user_id},'{name}',{is_worked}, '{start}', '{end}')"""
            save_log(query)
            return return_value
        except:
            error = traceback.format_exc()
            end = datetime.datetime.now(tz=datetime.timezone.utc)
            is_worked = 2
            # Unexpected error
            query = f"""INSERT INTO
                public.func_log (user_idx, func_code, is_worked, error_msg, start_time, end_time)
                VALUES ({user_id},'{name}',{is_worked}, '{error}', '{start}', '{end}')"""
            save_log(query)
            return traceback.format_exc()

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

    # 나머지 요소를 func으로부터 가져오기
    wrapper.__module__ = func.__module__
    wrapper.__doc__  = func.__doc__
    wrapper.__name__ = func.__name__
    wrapper.__qualname__ = func.__qualname__

    return wrapper