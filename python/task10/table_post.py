from database import Base, SessionLocal
from sqlalchemy import Column, Integer, String, Text, desc

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    topic = Column(String, nullable=True)

    def __repr__(self):
        return f"{self.id} - {self.topic}"

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
