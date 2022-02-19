from typing import Optional
from fastapi import Request, Query
import json
import numpy as np
import pandas as pd

async def set_transpose(item:Request) -> str:
    return pd.read_json(await item.json()).transpose().to_json()