
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql+asyncpg://postgres:2321@localhost:5432/postgres'
DATABASE_URL_SYNC = 'postgresql+psycopg2://postgres:2321@localhost:5432/postgres'
Base: DeclarativeMeta = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String)
    email = Column(String)
    role = Column(String)
    date = Column(String, default='unknow')
    salary = Column(String, default='30000')


metadata = Base.metadata
engine = create_async_engine(DATABASE_URL)
sync_engine = create_engine(DATABASE_URL_SYNC)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
sync_session_maker = sessionmaker(bind=sync_engine)


def get_sync_session():
    with sync_session_maker() as sync_session:
        return sync_session


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
