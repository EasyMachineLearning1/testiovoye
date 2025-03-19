#create-read-update-delete
from sqlalchemy.orm import Session
from app import models, schemas
from datetime import time, timedelta


def create_schedule(db: Session, schedule: schemas.ScheduleCreate):
    # Логика создания расписания
    # 1. Находим или создаем лекарство
    medicine = db.query(models.Medicine).filter(
        models.Medicine.name == schedule.medicine_name
    ).first()

    if not medicine:
        # Если лекарство не найдено, создаем новое
        medicine = models.Medicine(
            name=schedule.medicine_name,
            frequency=schedule.frequency,
            duration=schedule.duration
        )
        db.add(medicine)
        db.commit()
        db.refresh(medicine)

    # 2. Рассчитываем время начала и окончания
    start_time = time(8, 0)  # Начало приема в 8:00
    end_time = time(22, 0)   # Окончание приема в 22:00

    # 3. Рассчитываем интервал (в минутах)
    # Пример: если frequency = "каждые 2 часа", то interval_minutes = 120
    if "каждые" in schedule.frequency and "часа" in schedule.frequency:
        interval_minutes = int(schedule.frequency.split()[1]) * 60
    else:
        interval_minutes = 120  # Значение по умолчанию (2 часа)

    # 4. Создаем расписание
    db_schedule = models.Schedule(
        user_id=schedule.user_id,
        medicine_id=medicine.medicine_id,
        start_time=start_time,
        end_time=end_time,
        interval_minutes=interval_minutes
    )
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

def create_user(db: Session, name: str, policy_number: str):
    db_user = models.User(name=name, policy_number=policy_number)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user









def get_schedules(db: Session, user_id: int):
    return db.query(models.Schedule).filter(models.Schedule.user_id == user_id).all()

def get_schedule(db: Session, user_id: int, schedule_id: int):
    return db.query(models.Schedule).filter(
        models.Schedule.user_id == user_id,
        models.Schedule.schedule_id == schedule_id
    ).first()

from datetime import datetime, timedelta

def round_to_15_minutes(time_str: str) -> str:
    time = datetime.strptime(time_str, "%H:%M")
    rounded_minute = ((time.minute + 7) // 15) * 15
    return time.replace(minute=0, second=0) + timedelta(minutes=rounded_minute)