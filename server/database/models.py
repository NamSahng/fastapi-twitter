from sqlalchemy import (
    Column,
    Integer,
    String,
    TEXT,
    ForeignKey,
    DateTime,
    func
)
from sqlalchemy.orm import relationship
from database.db import Base

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(45), nullable=False)
    password = Column(String(128), nullable=False)
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    url = Column(TEXT, nullable=True)
    tweets = relationship("Tweets", back_populates="user")


class Tweets(Base):
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(TEXT, nullable=True)
    createdAt = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updatedAt = Column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())
    userId = Column(String(45), ForeignKey("users.id"), nullable=False)
    user = relationship("Users", back_populates="tweets")


# text vs varchar
# https://chuckolet.tistory.com/71

# relationship
# many to one
# https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
# many 부분에 foreign key를 설정한다
# back_pupulates에 다른 테이블의 relation 변수 명을 입력한다.