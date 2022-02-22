from optparse import Option
from typing import Optional
from click import option
from fastapi import Query, Request
from markupsafe import Markup
import numpy as np
import pandas as pd
# import modin.pandas as pd
import json
from bokeh.plotting import figure
from bokeh.embed import components, file_html
from bokeh.resources import CDN
from fastapi.templating import Jinja2Templates
import re



templates = Jinja2Templates(directory="visualization/templates")



async def box_plot(
    item : Request,                                         #data
    cols : Optional[str] = Query(None, max_length = 30),    #출력하고자하는 특성들(string)
    tools : Optional[str] = Query("", max_length= 20),      #...
    background_fill_color : Optional[str] = Query("#efefef", max_length= 16),
    fill_color1 : Optional[str] = Query("#E08E79", max_length= 16), #상자의 q2 ~ q3까지의 색깔 지정
    fill_color2 : Optional[str] = Query("#3B8686", max_length= 16) #상자의 q1 ~ q2까지의 색깔 지정
    ):

    #테스트 셋
    # df = pd.DataFrame({"a" : np.random.randn(2000), "b" : np.random.randn(2000), "c" : np.random.randn(2000), "d": np.random.randn(2000) })
    # cols = "a,b,c,d"

    df = pd.read_json(await item.json())
    # , " "를 구분자로 사용하여 분리하는 정규식을 차후 적용
    cols = list(re.split('[,]',cols))


    #각 특성별 특성명, 사분위 값, IQR, 이상치를 보관
    feature = []
    q1      = []
    q2      = []
    q3      = []
    iqr     = []
    upper   = []
    lower   = []
    out     = []

    #출력하고자하는 특성이 데이터프레임내에 존재하는지 확인
    for col in cols:
        if not col in df.columns:
            return {
                "stat" : 200,
                "body" : f"{col}이라는 특성이 없습니다. 가능 특성{df.columns}"
            }
        if df[col].dtype != np.float64 and df[col].dtype != np.float32 and df[col].dtype != np.int64 and df[col].dtype != np.int32:
             return {
                "stat" : 200,
                "body" : f"{col}이라는 특성은 숫자형 자료가 아닙니다."
            }
        feature.append(col)

    #plot의 x축을 특성명으로 설정
    plot = figure(tools=tools, background_fill_color=background_fill_color, x_range=feature)

    #각 특성별 사분위, IQR값을 저장 및 이상치 출력
    for col in feature:

        q1.append(df[col].quantile(q=0.25))
        q2.append(df[col].quantile(q=0.5))
        q3.append(df[col].quantile(q=0.75))
        iqr.append(q3[-1] - q1[-1])
        upper.append(q3[-1] + 1.5*iqr[-1])
        lower.append(q1[-1] - 1.5*iqr[-1])

        # 이상치 계산
        out.append(list(df[(df[col] > upper[-1]) | (df[col] < lower[-1])][col]))

        # 이상치 출력
        if len(out[-1]) != 0:
            plot.circle([col]*len(out[-1]), out[-1], size=6, color="#F38630", fill_alpha=0.6)


    #상자그림의 줄기
    plot.segment(x0=feature, y0=upper, x1=feature, y1=q3, line_color="black")
    plot.segment(x0=feature, y0=lower, x1=feature, y1=q1, line_color="black")

    # 상자
    plot.vbar(x=feature, width = [0.7] * len(feature), bottom = q2, top = q3, fill_color=fill_color1, line_color="black")
    plot.vbar(x=feature, width = [0.7] * len(feature), bottom = q1, top = q2, fill_color=fill_color2, line_color="black")

    # 수염
    plot.rect(x=feature, y = lower, width = [0.2] * len(feature), height = [0.01] * len(feature), line_color="black")
    plot.rect(x=feature, y = upper, width = [0.2] * len(feature), height = [0.01] * len(feature), line_color="black")

    #plot의 그리드 설정(차후 세분화된 기능을 넣을시 이에 대한 확장 필요)
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = "white"
    plot.grid.grid_line_width = 2
    plot.xaxis.major_label_text_font_size="16px"

    script, div = components(plot)
    return script, div


async def hist_plot(
    item : Request,                                         #data
    col : Optional[str] = Query(None, max_length = 30)
):

    df = pd.read_json(await item.json())

    #출력하고자하는 특성이 데이터프레임내에 존재하는지 확인
    if not col in df.columns:
        return {
                "stat" : 200,
                "body" : f"{col}이라는 특성이 없습니다. 가능 특성{df.columns}"
            }


    #col이라는 특성이 숫자형인지 확인
    if df[col].dtype != np.float64 and df[col].dtype != np.float32 and df[col].dtype != np.int64 and df[col].dtype != np.int32:
            return {
            "stat" : 200,
            "body" : f"{col}이라는 특성은 숫자형 자료가 아닙니다."
        }

    #해당 특성의 데이터를 히스토그램으로 변환
    hist, edges = np.histogram(df[col], density=True, bins=50)
    plot = figure(tools='', background_fill_color="#fafafa")
    plot.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color="navy", line_color="white", alpha=0.5)

    plot.y_range.start = 0
    plot.xaxis.axis_label = "x_col"
    plot.yaxis.axis_label = "y_col"
    plot.grid.grid_line_color="white"

    script, div = components(plot)
    return script, div


async def count_plot(
    item : Request,                                         #data
    col : Optional[str] = Query(None, max_length = 30),
    title : Optional[str] = Query("title", max_length = 30),
    height : Optional[str] = Query("250", max_length = 5),
    width : Optional[str] = Query("0.9", max_length = 5),
):

    df = pd.read_json(await item.json())


    #출력하고자하는 특성이 데이터프레임내에 존재하는지 확인
    if not col in df.columns:
        return {
                "stat" : 200,
                "body" : f"{col}이라는 특성이 없습니다. 가능 특성{df.columns}"
            }
    #해당 특성의 데이터 타입이 문자열인지 확인
    if df[col].dtype == np.float64 or df[col].dtype == np.float32 or df[col].dtype == np.int64 or df[col].dtype == np.int32:
            return {
            "stat" : 200,
            "body" : f"{col}이라는 특성은 문자형 자료가 아닙니다."
        }

    #각 데이터별 갯수
    cnt = df[col].value_counts()
    feature = list(cnt.index)
    cnt = list(cnt)

    #plot의 길이 및 기타 설정
    height = int(height)
    plot = figure(tools="", x_range=feature, height=height, title=title)

    width = float(width)
    plot.vbar(x=feature, top=cnt, width=width)

    plot.xgrid.grid_line_color = None
    plot.y_range.start = 0

    script, div = components(plot)
    return script, div



async def scatter_plot(
    item : Request,
    x_col : Optional[str] = Query(None, max_length = 30),
    y_col : Optional[str] = Query(None, max_length = 30)
    ):

    #json -> dataframe
    df = pd.read_json(await item.json())

    # x_col이라는 특성이 존재하는지 확인
    if not x_col in df.columns:
        return {
                "stat" : 200,
                "body" : f"{x_col}이라는 특성이 없습니다. 가능 특성{df.columns}"
            }

    # y_col이라는 특성이 존재하는지 확인
    if not y_col in df.columns:
        return {
                "stat" : 200,
                "body" : f"{y_col}이라는 특성이 없습니다. 가능 특성{df.columns}"
            }


    #x_col이라는 특성이 카테고리일때 해당 범주에 맞게 plot을 x범위 설정
    x_range = None
    if df[x_col].dtype != np.float64 and df[x_col].dtype != np.float32 and df[x_col].dtype != np.int64 and df[x_col].dtype != np.int32:
            x_range = list(df[x_col].unique())


    #y_col이라는 특성이 카테고리일때 해당 범주에 맞게 plot을 y범위 설정
    y_range = None
    if df[y_col].dtype != np.float64 and df[y_col].dtype != np.float32 and df[y_col].dtype != np.int64 and df[y_col].dtype != np.int32:
            y_range = list(df[y_col].unique())


    p = figure(tools="", background_fill_color="#efefef", x_range=x_range , y_range=y_range)
    p.circle(df[x_col], df[y_col], size=2, color="#F38630", fill_alpha=0.6)


    p.xgrid.grid_line_color = "white"
    p.ygrid.grid_line_color = "white"
    p.grid.grid_line_width = 2
    p.xaxis.major_label_text_font_size="16px"

    script, div = components(p)
    return script, div


async def bar_plot(item : Request):
    pass
