from sqlalchemy import Column, String, Time, Integer, ForeignKey
from sqlalchemy.orm import declarative_base

# Создаем базовый класс для моделей
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key = True, index = True)
    name = Column(String, nullable = False)
    policy_number = Column(String, unique = True, nullable = False)

class Medicine(Base):
    __tablename__ = "medicines"
    medicine_id = Column(Integer, primary_key = True, index = True)
    name = Column(String,nullable = False)
    frequency = Column(String, nullable = False)
    duration = Column(String, nullable = False)

class Schedule(Base):
    __tablename__ = "schedules"
    schedule_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    medicine_id = Column(Integer, ForeignKey("medicines.medicine_id"))
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    interval_minutes = Column(Integer, nullable=False)