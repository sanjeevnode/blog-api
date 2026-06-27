from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy_utils import UUIDType

from app.core.utils.database_types import ISTDateTime
from app.core.utils.timezone import get_ist_now

# Explicit naming conventions for constraints.
# Postgres requires names for constraints (like index names, foreign key names).
# Defining this here guarantees SQLAlchemy and Alembic generate them consistently.
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)


class Base(DeclarativeBase):
    metadata = metadata

    # Automatically generate __tablename__ based on class name in lowercase
    @declared_attr.directive
    def __tablename__(self) -> str:
        return self.__name__.lower()

    # UUID primary key (stored as VARCHAR or BINARY(16) but parsed as UUID in Python)
    id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(binary=False), primary_key=True, default=uuid.uuid4
    )
    
    # Audit timestamps using our custom timezone-aware ISTDateTime type
    created_at: Mapped[datetime] = mapped_column(
        ISTDateTime(), default=get_ist_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        ISTDateTime(), default=get_ist_now, onupdate=get_ist_now, nullable=False
    )
