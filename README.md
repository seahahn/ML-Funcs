# ❇️ AI Play ML-Funcs

API server for all machine learning-related functions except model training.

## :one: Stack

- Python 3.8.12
- FastAPI 0.73.0
- Pandas 1.4.1
- scikit-learn 1.0.2
- JWT
- Swagger

<br/>

## :two: Deployment Platform and Server Address

- Platform: Heroku
- Address: [https://aiplay-mlfuncs.herokuapp.com/](https://aiplay-mlfuncs.herokuapp.com/)

<br/>

## :three: API Specification

- DOCS: [https://aiplay-mlfuncs.herokuapp.com/docs](https://aiplay-mlfuncs.herokuapp.com/docs)

<details>
  <summary>Expand</summary>

| Method | URL                             | Description                                                           |
| ------ | ------------------------------- | --------------------------------------------------------------------- |
| POST   | /uploadfile                     | Upload dataset and convert to JSON                                    |
| POST   | /dataframe/head                 | Display the first N rows of the DataFrame                             |
| POST   | /dataframe/tail                 | Display the last N rows of the DataFrame                              |
| POST   | /dataframe/shape                | Display the number of rows and columns of the DataFrame               |
| POST   | /dataframe/dtype                | Display the type of each column in the DataFrame                      |
| POST   | /dataframe/columns              | Display the list of columns in the DataFrame                          |
| POST   | /dataframe/unique               | Display the list of unique values in a column                         |
| POST   | /dataframe/isna                 | Check for missing values in the DataFrame                             |
| POST   | /dataframe/corr                 | Display the correlation coefficients between columns in the DataFrame |
| POST   | /dataframe/describe             | Display the statistical summary of the DataFrame                      |
| POST   | /dataframe/col_condition        | Display data based on numerical conditions                            |
| POST   | /dataframe/loc                  | Display data based on index or column name conditions                 |
| POST   | /dataframe/iloc                 | Display data based on index or column order conditions                |
| POST   | /dataframe/transpose            | Transpose rows and columns of the DataFrame                           |
| POST   | /dataframe/groupby              | Group data according to specified conditions                          |
| POST   | /dataframe/drop                 | Remove rows or columns based on specified conditions                  |
| POST   | /dataframe/dropna               | Remove missing values from the DataFrame                              |
| POST   | /dataframe/rename               | Rename columns in the DataFrame                                       |
| POST   | /dataframe/sort_values          | Sort the DataFrame data according to specified conditions             |
| POST   | /dataframe/merge                | Merge two DataFrames based on specified conditions                    |
| POST   | /dataframe/concat               | Concatenate two DataFrames based on specified conditions              |
| POST   | /dataframe/set_column           | Create a new column based on specified conditions                     |
| POST   | /dataframe/feature_target_split | Separate features and target in the DataFrame                         |
| POST   | /dataframe/train_test_split     | Split the dataset into training, validation, and test sets            |
| POST   | /plot/boxplot                   | Visualize boxplots                                                    |
| POST   | /plot/histplot                  | Visualize histograms                                                  |
| POST   | /plot/countplot                 | Visualize frequency graphs                                            |
| POST   | /plot/scatterplot               | Visualize scatter plots                                               |

</details>

<br/>

## :four: Troubleshooting Records

- [https://github.com/AI-Play/ML-Funcs/discussions](https://github.com/AI-Play/ML-Funcs/discussions)

<br/>

## :five: Development Environment Preparation

<details>
  <summary>Expand</summary>

```
// Create a new virtual environment
// 1. Move to the directory which has python version we need to use
// 2. Create a new virtual environment
python -m venv /path/to/new/virtual/environment

// 3. Activate the virtual environment
source /path/to/new/virtual/environment/bin/activate

// 4. Install required packages
pip install -r requirements.txt
```

##### Run

```
export MODIN_ENGINE=ray   # Modin will use Ray
export MODIN_ENGINE=dask  # Modin will use Dask

uvicorn main:app --reload
```

</details>
