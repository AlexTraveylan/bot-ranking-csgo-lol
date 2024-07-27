import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

TEST_DATABASE_URL = "sqlite:///:memory:"


engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def db_session():
    SQLModel.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    SQLModel.metadata.drop_all(bind=engine)
