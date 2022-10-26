from database import Base, SessionLocal
from sqlalchemy import Column, Integer, String, desc

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    topic = Column(String)

if __name__ == '__main__':
    session = SessionLocal()
    query_1 = (
        session.query(Post)
        .filter(Post.topic == 'business')
        .order_by(desc(Post.id))
        .limit(10)
        .all()
    )
    result = [i.id for i in query_1]

    print(result)
