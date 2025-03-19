#схемы для валидации данных
from pydantic import BaseModel
from datetime import time

class ScheduleCreate(BaseModel):
    medicine_name: str
    frequency: str  # Например, "каждые 2 часа" или "3 раза в день"
    duration: str   # Например, "2 недели" или "постоянно"
    user_id: int

class ScheduleResponse(BaseModel):
    schedule_id: int
    user_id: int
    medicine_id: int
    start_time: time
    end_time: time
    interval_minutes: int

class MedicineCreate(BaseModel):
    name: str
    frequency: str
    duration: str