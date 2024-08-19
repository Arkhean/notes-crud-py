from datetime import datetime

from sqlalchemy import create_engine, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Mapped
from sqlalchemy.testing.schema import mapped_column

engine = create_engine("sqlite:///database.sqlite")
Session = sessionmaker(engine)


def get_db():
    with Session() as db:
        yield db


# Tables ===============================================================================================================

Base = declarative_base()


class Note(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
