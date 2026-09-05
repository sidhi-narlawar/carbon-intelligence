from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./carbon.db"

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


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    activity_type = Column(String)
    amount = Column(Float)
    unit = Column(String)
    scope = Column(Integer)
    emission_factor = Column(Float)
    emissions = Column(Float)
    date = Column(String)

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category = Column(String)
    emissions = Column(Float)
    carbon_score = Column(Float)

    
Base.metadata.create_all(bind=engine)