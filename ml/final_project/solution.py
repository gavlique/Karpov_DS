import pandas as pd
from sqlalchemy import create_engine
import os
import hashlib
from loguru import logger
from catboost import CatBoostClassifier
from schema import PostGet, Response
from typing import List
from fastapi import FastAPI
from datetime import datetime


app = FastAPI()

LOCAL_PATH = r"D:\Coding\Karpov_DS\ml\final_project"


def get_exp_group(user_id: int) -> str:
    user_str = (str(user_id) + 'experiment').encode() # to UTF-8
    hash_numeric = int(hashlib.md5(user_str).hexdigest(), base=16)
    return 'control' if hash_numeric % 2 == 0 else 'test'


def get_model_path(path: str) -> str:
    # проверяем где выполняется код в лмс, или локально. Немного магии
    if os.environ.get("IS_LMS") == "1":
        MODEL_PATH = '/workdir/user_input'
    else:
        MODEL_PATH = path
    return MODEL_PATH


def load_models(version: str) -> CatBoostClassifier:
    model_path = os.path.join(get_model_path(LOCAL_PATH), f"model_{version}")
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
model_test = load_models('test')
model_control = load_models('control')
logger.info('loading_features')
features = load_features()
logger.info('service is ready')


@app.get("/post/recommendations/", response_model=Response)
def recommended_posts(
        id: int,
        time: datetime,
        limit: int = 10) -> Response:
    # Юзеры
    logger.info(f'user_id: {id}')
    
    logger.info('getting group and selecting model')
    exp_group = get_exp_group(id)

    if exp_group == 'test':
        model = model_test
    else:
        model = model_control


    logger.info('reading features')
    user_features = features[2].loc[features[2].user_id == id]
    if exp_group == 'test':
        user_features = user_features.drop('user_id', axis=1)
    else:
        user_features = user_features.drop([
            'user_id',
            'gender'
        ]
        , axis=1)

    # Посты
    logger.info('dropping columns')
    content = features[1].copy()
    if exp_group == 'test':
        post_features = features[1].drop('text', axis=1)
    else:
        post_features = features[1][[
            'post_id',
            'topic'
        ]]


    # Присоединяем к фичам по конкретному пользователю
    logger.info('zipping everything')
    add_user_features = dict(zip(user_features.columns, user_features.values[0]))
    user_posts_features = post_features.assign(**add_user_features)
    user_posts_features = user_posts_features.set_index('post_id')

    # Временные характеристики
    if exp_group == 'test':
        logger.info('add time info')
        user_posts_features['hour'] = time.hour
        user_posts_features['month'] = time.month
    
    # Погнали предсказывать

    logger.info('predicting')
    prediction = model.predict_proba(user_posts_features)[:, 1]
    user_posts_features['prediction'] = prediction

    liked_posts = features[0][features[0].user_id == id].post_id.values
    user_posts_features = user_posts_features[~user_posts_features.index.isin(liked_posts)]

    recommendations = user_posts_features.sort_values('prediction', ascending=False)[:limit].index

    return Response(exp_group=exp_group, recommendations=[
        PostGet(**{
            "id": i,
            "text": content[content.post_id == i].text.values[0],
            "topic": content[content.post_id == i].topic.values[0]
        }) for i in recommendations
    ])
