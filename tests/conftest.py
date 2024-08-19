import pytest

from app.db import Base, engine


@pytest.fixture(autouse=True, scope="function")
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
