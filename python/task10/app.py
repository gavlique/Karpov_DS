from fastapi import FastAPI, HTTPException, Depends
from datetime import date, timedelta
from typing import List, Dict
from schema import UserGet, PostGet, FeedGet
from table_feed import Feed
from table_post import Post
from table_user import User
from database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

app = FastAPI()

def get_db():
    return SessionLocal()

@app.get('/user/{id}', response_model=UserGet)
def get_user(id: int, db: Session = Depends(get_db)):
    result = db.query(User).filter(User.id == id).one_or_none() 
    if result:
        return result
    else:
        raise HTTPException(404)
    

@app.get('/post/{id}', response_model=PostGet)
def get_post(id: int, db: Session = Depends(get_db)):
    result = db.query(Post).filter(Post.id == id).one_or_none()
    if result:
        return result
    else:
        raise HTTPException(404)

@app.get('/user/{id}/feed', response_model=List[FeedGet])
def get_post(id: int, limit: int = 10, db: Session = Depends(get_db)):
    result = db.query(Feed).filter(Feed.user_id == id).order_by(desc(Feed.time)).limit(limit).all()
    return result

@app.get('/post/{id}/feed', response_model=List[FeedGet])
def get_post(id: int, limit: int = 10, db: Session = Depends(get_db)):
    result = db.query(Feed).filter(Feed.post_id == id).order_by(desc(Feed.time)).limit(limit).all()
    return result


@app.get('/post/recommendations/')
def get_recommendations(id: int, limit: int = 10, db: Session = Depends(get_db)):
    result = (
        db.query(Post)
        .select_from(Feed)
        .filter(Feed.action == 'like')
        .join(Post)
        .group_by(Post.id)
        .order_by(desc(func.count(Post.id)))
        .limit(limit)
        .all()
    )
    return result