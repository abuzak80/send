from sqlalchemy import DDL, Connection, MetaData, Table, event
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .settings import settings

SCHEMA_NAME = "interview"

POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

engine = create_async_engine(settings.db_connection_string, echo=False)
session = async_sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=engine
)
metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)


class Base(DeclarativeBase):
    metadata = metadata


@event.listens_for(Table, "before_create")
def create_schema_if_not_exists(target: Table, connection: Connection, **_):
    connection.execute(
        DDL('CREATE SCHEMA IF NOT EXISTS "%(schema)s"', {"schema": target.schema})
    )


async def get_db():
    async with session() as db:
        yield db
