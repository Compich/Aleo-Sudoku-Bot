from contextlib import asynccontextmanager
from typing import Annotated, List, Union

import sqlalchemy as sa
from sqlalchemy import func, select, text, update
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase, joinedload

import config

int64 = Annotated[int, 8]
str_40 = Annotated[str, 40]
str_53 = Annotated[str, 53]
str_59 = Annotated[str, 59]
str_81 = Annotated[str, 81]
str_100 = Annotated[str, 100]
str_128 = Annotated[str, 128]
str_255 = Annotated[str, 255]

engine = create_async_engine(
    f'postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}@' +
    f'{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}',
    echo=False
)

async_session = async_sessionmaker(engine, expire_on_commit=False)


@asynccontextmanager
async def session_pool():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise


class Base(DeclarativeBase):
    type_annotation_map = {
        float: sa.Double(),
        int64: sa.BigInteger(),
        str_40: sa.String(40),
        str_53: sa.String(53),
        str_59: sa.String(59),
        str_81: sa.String(81),
        str_100: sa.String(100),
    }

    @classmethod
    def primary_key(cls):
        return inspect(cls).primary_key[0]

    async def delete(self):
        async with session_pool() as session:
            return await session.delete(self)

    async def update(self, **kwargs):
        pk = self.primary_key().name
        pk_value = getattr(self, pk)
        async with session_pool() as session:
            await session.execute(
                update(
                    type(self)
                ).where(
                    text(f"{pk} = '{pk_value}'")
                ).values(
                    **kwargs
                )
            )
        return await type(self).get_pk(pk_value)

    @classmethod
    def get_options(cls):
        options = []

        relationships = inspect(cls).relationships
        for relationship in relationships:
            options.append(joinedload(relationship))

        return options

    @classmethod
    async def get(
        cls,
        filter_statement=None,
        limit: int = 1,
        order_by=None
    ) -> Union['Base', List['Base']]:
        statement = select(cls)
        if filter_statement is not None:
            statement = statement.where(filter_statement)

        statement = statement.options(*cls.get_options()).limit(limit)

        if order_by:
            statement = statement.order_by(order_by)

        async with session_pool() as session:
            if limit and limit == 1:
                return await session.scalar(statement)

            return (await session.scalars(statement)).unique().all()

    @classmethod
    async def get_all(cls, filter_statement=None, order_by=None) -> List['Base']:
        return await cls.get(filter_statement, limit=None, order_by=order_by)

    @classmethod
    async def get_pk(cls, pk_value) -> 'Base':
        pk = cls.primary_key().name
        return await cls.get(getattr(cls, pk) == pk_value)

    @classmethod
    async def count(cls, filter_statement=None) -> 'Base':
        statement = select(func.count()).select_from(cls)
        if filter_statement is not None:
            statement = statement.where(filter_statement)
        async with session_pool() as session:
            return await session.scalar(statement)

    @classmethod
    async def add_new(cls, **kwargs) -> 'Base':
        new_obj = cls(**kwargs)
        async with session_pool() as session:
            session.add(new_obj)
        return new_obj
