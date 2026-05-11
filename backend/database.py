from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database
DATABASE_URL = "sqlite:///./crm.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# TABLE
class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)

    hcp_name = Column(String)
    interaction_type = Column(String)
    date = Column(String)
    time = Column(String)
    attendees = Column(String)
    topics = Column(String)
    materials = Column(String)
    sentiment = Column(String)
    outcome = Column(String)


# CREATE TABLE
Base.metadata.create_all(bind=engine)