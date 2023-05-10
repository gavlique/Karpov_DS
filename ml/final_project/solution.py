import pandas as pd
from sqlalchemy import create_engine
import os
from catboost import CatBoostClassifier
from schema import PostGet
from typing import List
from fastapi import FastAPI
from datetime import datetime

app = FastAPI()


def get_model_path(path: str) -> str:
    # проверяем где выполняется код в лмс, или локально. Немного магии
    if os.environ.get("IS_LMS") == "1":
        MODEL_PATH = '/workdir/user_input/model'
    else:
        MODEL_PATH = path
    return MODEL_PATH


def load_models():
    model_path = get_model_path(os.getcwd() + "/model")
    # LOAD MODEL HERE PLS :)
    # здесь не указываем параметры, которые были при обучении, в дампе модели все есть
    from_file = CatBoostClassifier()

    from_file.load_model(model_path)

    return from_file


def batch_load_sql(query: str) -> pd.DataFrame:
    CHUNKSIZE = 200000
    engine = create_engine(
        "postgresql://robot-startml-ro:pheiph0hahj1Vaif@"
        "postgres.lab.karpov.courses:6432/startml"
    )
    conn = engine.connect().execution_options(stream_results=True)
    chunks = []
    for chunk_dataframe in pd.read_sql(query, conn, chunksize=CHUNKSIZE):
        chunks.append(chunk_dataframe)
    conn.close()
    return pd.concat(chunks, ignore_index=True)


def load_features():
    liked_posts = batch_load_sql("""
        SELECT 
            distinct post_id, user_id
        FROM
            public.feed_data
        WHERE 
            action = 'like'
    """)

    post_features = batch_load_sql("""
        SELECT 
            post_id,
            topic
        FROM
            public.post_text_df
    """)

    user_features = batch_load_sql("""
        SELECT 
            user_id,
            age, 
            city,
            exp_group
        FROM
            public.user_data
    """)

    return liked_posts, post_features, user_features

@app.get("/post/recommendations/", response_model=List[PostGet])
def recommended_posts(
        id: int,
        time: datetime,
        limit: int = 10) -> List[PostGet]:
    # На время забьем хуй

