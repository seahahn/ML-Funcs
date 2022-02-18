# AI-Play ML-Funcs
**(추가되는 내용에 맞춰 지속 수정 필요)**

머신 러닝 관련 기능 중 모델 학습을 제외한 모든 기능을 위한 API 서버

## Stack

Python 3.8.12  
[FastAPI 0.73.0](fastapi.tiangolo.com)

## 준비 사항

```
pip install fastapi uvicorn[standard]
```

## 실행

```
export MODIN_ENGINE=ray   # Modin will use Ray
export MODIN_ENGINE=dask  # Modin will use Dask

uvicorn main:app --reload
```