import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base

def get_engine():
    # If using Streamlit Secrets for production
    try:
        if "DATABASE_URL" in st.secrets:
            db_url = st.secrets["DATABASE_URL"]
            # Fix for SQLAlchemy 1.4+ with postgresql uri
            if db_url.startswith("postgres://"):
                db_url = db_url.replace("postgres://", "postgresql://", 1)
            engine = create_engine(db_url)
            Base.metadata.create_all(engine)
            return engine
    except Exception:
        pass
    
    # Local SQLite development
    engine = create_engine("sqlite:///naye_pankh.db", connect_args={"check_same_thread": False})
    
    # Create all tables
    Base.metadata.create_all(engine)
    return engine

def get_session():
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()
