# ❇️ AI Play ML-Funcs

머신 러닝 관련 기능 중 모델 학습을 제외한 모든 기능을 위한 API 서버

## :one: Stack

- Python 3.8.12
- FastAPI 0.73.0
- Pandas 1.4.1
- scikit-learn 1.0.2
- JWT
- Swagger

<br/>

## :two: 배포 플랫폼 및 서버 주소

- 플랫폼 : Heroku
- 주소 : https://aiplay-mlfuncs.herokuapp.com/

<br/>

## :three: API 명세

- DOCS : https://aiplay-mlfuncs.herokuapp.com/docs

<details>
  <summary>펼쳐보기</summary>

| Method | URL                             | Description                                         |
| ------ | ------------------------------- | --------------------------------------------------- |
| POST   | /uploadfile                     | 데이터셋 업로드 및 JSON 변환                        |
| POST   | /dataframe/head                 | 데이터프레임의 처음 N개 행 출력                     |
| POST   | /dataframe/tail                 | 데이터프레임의 마지막 N개 행 출력                   |
| POST   | /dataframe/shape                | 데이터프레임의 행, 열 갯수 출력                     |
| POST   | /dataframe/dtype                | 데이터프레임의 컬럼별 타입 출력                     |
| POST   | /dataframe/columns              | 데이터프레임의 컬럼 목록 출력                       |
| POST   | /dataframe/unique               | 컬럼 내 고유값 목록 출력                            |
| POST   | /dataframe/isna                 | 데이터프레임의 결측치 확인                          |
| POST   | /dataframe/corr                 | 데이터프레임의 컬럼별 상관계수 확인                 |
| POST   | /dataframe/describe             | 데이터프레임의 통계 수치 확인                       |
| POST   | /dataframe/col_condition        | 수치 조건에 맞는 데이터 출력                        |
| POST   | /dataframe/loc                  | 인덱스 혹은 컬럼명 조건에 해당하는 데이터 출력      |
| POST   | /dataframe/iloc                 | 인덱스 혹은 컬럼 순서값 조건에 해당하는 데이터 출력 |
| POST   | /dataframe/transpose            | 데이터프레임의 행/열 전환                           |
| POST   | /dataframe/groupby              | 조건에 맞게 데이터 그룹으로 묶기                    |
| POST   | /dataframe/drop                 | 조건에 맞는 행 또는 열 제거                         |
| POST   | /dataframe/dropna               | 데이터프레임 결측치 제거                            |
| POST   | /dataframe/rename               | 데이터프레임 컬럼명 변경                            |
| POST   | /dataframe/sort_values          | 조건에 맞춰 데이터프레임의 데이터 정렬              |
| POST   | /dataframe/merge                | 조건에 맞춰 2개의 데이터프레임 합치기               |
| POST   | /dataframe/concat               | 조건에 맞춰 2개의 데이터프레임 이어붙이기           |
| POST   | /dataframe/set_column           | 조건에 맞춰 새로운 컬럼 생성                        |
| POST   | /dataframe/feature_target_split | 특성 / 타겟 분리하기                                |
| POST   | /dataframe/train_test_split     | 훈련 / 검증 / 테스트셋 분리하기                     |
| POST   | /plot/boxplot                   | 상자 수염 그림 시각화                               |
| POST   | /plot/histplot                  | 히스토그램 시각화                                   |
| POST   | /plot/countplot                 | 빈도 그래프 시각화                                  |
| POST   | /plot/scatterplot               | 산점도 시각화                                       |

</details>

<br/>

## :four: 트러블 슈팅 기록

- https://github.com/AI-Play/ML-Funcs/discussions

<br/>

## :five: 개발 환경 준비 사항

<details>
  <summary>펼쳐보기</summary>

```
# 새 가상환경 만들기
# 1. 사용해야 할 python version이 있는 디렉토리로 이동
# 2. 새 가상환경 생성을 위한 명령어 실행
python -m venv /path/to/new/virtual/environment

# 3. 가상환경 활성화하기
source /path/to/new/virtual/environment/bin/activate

# 4. 필요한 패키지 설치
pip install -r requirements.txt
```

##### 실행

```
export MODIN_ENGINE=ray   # Modin will use Ray
export MODIN_ENGINE=dask  # Modin will use Dask

uvicorn main:app --reload
```

</details>
