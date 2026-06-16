from sqlalchemy import Column, Integer, String, Boolean, Date, Float, Text, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()

# Association table for Programs and Beneficiaries
program_beneficiary = Table(
    'program_beneficiary',
    Base.metadata,
    Column('program_id', Integer, ForeignKey('programs.id'), primary_key=True),
    Column('beneficiary_id', Integer, ForeignKey('beneficiaries.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    role = Column(String(20), default='viewer')  # 'admin' or 'viewer'

class Volunteer(Base):
    __tablename__ = 'volunteers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    city = Column(String(50), nullable=False)
    skills = Column(String(200))
    is_active = Column(Boolean, default=True)
    join_date = Column(Date, default=func.current_date())

class Beneficiary(Base):
    __tablename__ = 'beneficiaries'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer)
    gender = Column(String(20))
    education_level = Column(String(50))
    location = Column(String(100))
    status = Column(String(20), default='active')  # active, completed, dropout

class Donation(Base):
    __tablename__ = 'donations'
    
    id = Column(Integer, primary_key=True)
    donor_name = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, default=func.current_date())
    purpose = Column(String(100))
    payment_mode = Column(String(50))

class Program(Base):
    __tablename__ = 'programs'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    description = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String(20), default='upcoming')  # upcoming, ongoing, completed
    
    beneficiaries = relationship('Beneficiary', secondary=program_beneficiary, backref='programs')
