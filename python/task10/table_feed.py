from database import Base, SessionLocal
from table_post import Post
from table_user import User
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, desc


class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, ForeignKey=User.id)
    post_id = Column(Integer, ForeignKey=Post.id)
    action = Column(String)
    time = Column(DateTime)
