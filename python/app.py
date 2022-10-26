from fastapi import FastAPI, HTTPException, Depends
from datetime import date, timedelta
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

class User(BaseModel):
    name: str
    surname: str 
    age: int
    registration_date: date

    class Config:
        orm_mode = True

app = FastAPI()

# @app.get('/')
# def hello():
#     return 'hello, world'

class PostResponse(BaseModel):
    id: int
    text: str
    topic: str

    class Config:
        orm_mode = True


@app.get('/')
def sum(a: int, b: int) -> int:
    return a + b

@app.get('/sum_date')
def sum_date(current_date: date, offset: int):
    return current_date + timedelta(days=offset)

@app.post('/user/validate')
def post_user(json: User):
    if isinstance(json, User):
        return f"Will add user: {json.name} {json.surname} with age {json.age}"
    else:
        raise HTTPException(422)

def get_db():
    conn = psycopg2.connect(
        "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml",
        cursor_factory=RealDictCursor
    )
    return conn

@app.get('/user/{id}')
def user_data(id, db = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(f"""
        select gender, age, city
        from "user"
        where id = {id}
    """)
    result = cursor.fetchone()

    cursor.close()
    db.close()

    if not result:
        raise HTTPException(404, "user not found")
    else:
        return result

@app.get('/post/{id}', response_model=PostResponse)
def validate_user(id, db = Depends(get_db)) -> PostResponse:
    with db.cursor() as cursor:
        cursor.execute(f"""
            select id, text, topic
            from "post"
            where id = {id}
        """)
        result = cursor.fetchone()

        if not result:
            raise HTTPException(404, "user not found")
        else:
            return PostResponse(**result)
