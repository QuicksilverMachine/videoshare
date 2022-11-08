import uuid
from typing import Any

from flask import request
from sqlalchemy import CHAR, TypeDecorator
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql.psycopg2 import PGDialect_psycopg2
from sqlalchemy.dialects.sqlite.pysqlite import SQLiteDialect_pysqlite

from videoshare.errors import BadRequest


def get_request_json() -> dict[str, Any]:
    if not request.json or not isinstance(request.json, dict):
        raise BadRequest("Invalid JSON data")
    return request.json


class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """

    impl = CHAR
    cache_ok = True

    def load_dialect_impl(
        self, dialect: PGDialect_psycopg2 | SQLiteDialect_pysqlite
    ) -> Any:
        print("DIALECT", type(dialect))
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID(as_uuid=True))  # type: ignore
        else:
            return dialect.type_descriptor(CHAR(32))  # type: ignore

    def process_bind_param(
        self,
        value: str | uuid.UUID | None,
        dialect: PGDialect_psycopg2 | SQLiteDialect_pysqlite,
    ) -> Any:
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hex string
                return "%.32x" % value.int

    def process_result_value(
        self,
        value: str | uuid.UUID | None,
        dialect: PGDialect_psycopg2 | SQLiteDialect_pysqlite,
    ) -> Any:
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value
