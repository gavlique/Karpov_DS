import pandas as pd
from sqlalchemy import create_engine
import os
from loguru import logger
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
    model_path = get_model_path(os.getcwd() + r"\model")
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
    logger.info('feed is ready')

    post_features = batch_load_sql("""
        SELECT
            *
        FROM
            d_gavlovskij_features_lesson_22
    """)
    logger.info('posts are ready')

    user_features = batch_load_sql("""
        SELECT 
            user_id,
            gender,
            age, 
            city,
            exp_group
        FROM
            public.user_data
    """)
    logger.info('users are ready')

    return liked_posts, post_features, user_features

logger.info('loading_models')
model = load_models()
logger.info('loading_features')
features = load_features()
logger.info('service is ready')


@app.get("/post/recommendations/", response_model=List[PostGet])
def recommended_posts(
        id: int,
        time: datetime,
        limit: int = 10) -> List[PostGet]:
    # Юзеры
    logger.info(f'user_id: {id}')
    logger.info('reading features')
    user_features = features[2].loc[features[2].user_id == id]
    user_features = user_features.drop('user_id', axis=1)

    # Посты
    logger.info('dropping columns')
    content = features[1].copy()
    post_features = features[1].drop('text', axis=1)


    # Присоединяем к фичам по конкретному пользователю
    logger.info('zipping everything')
    add_user_features = dict(zip(user_features.columns, user_features.values[0]))
    user_posts_features = post_features.assign(**add_user_features)
    user_posts_features = user_posts_features.set_index('post_id')

    # Временные характеристики
    logger.info('add time info')
    user_posts_features['hour'] = time.hour
    user_posts_features['month'] = time.month
    
    # Погнали предсказывать
    logger.info(user_posts_features.info())

    logger.info('predicting')
    prediction = model.predict_proba(user_posts_features)[:, 1]
    user_posts_features['prediction'] = prediction

    liked_posts = features[0][features[0].user_id == id].post_id.values
    user_posts_features = user_posts_features[~user_posts_features.index.isin(liked_posts)]

    recommendations = user_posts_features.sort_values('prediction', ascending=False)[:limit].index


    return [
        PostGet(**{
            "id": i,
            "text": content[content.post_id == i].text.values[0],
            "topic": content[content.post_id == i].topic.values[0]
        }) for i in recommendations
    ]
