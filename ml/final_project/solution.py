import os
from catboost import CatBoostClassifier

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
