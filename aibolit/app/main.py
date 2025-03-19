from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import SessionLocal, engine


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind = engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API доктора Айболита"}


@app.post("/schedule/", response_model=schemas.ScheduleResponse)
def create_schedule(schedule: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли пользователь
    user = db.query(models.User).filter(models.User.user_id == schedule.user_id).first()
    if not user:
        # Если пользователь не существует, создаем его
        user = crud.create_user(db, name="Иван Иванов", policy_number="123456789")
    
    # Создаем расписание
    return crud.create_schedule(db=db, schedule=schedule)

# Роут для получения списка расписаний
@app.get("/schedules/", response_model=list[schemas.ScheduleResponse])
def read_schedules(user_id: int, db: Session = Depends(get_db)):
    schedules = crud.get_schedules(db, user_id=user_id)
    if not schedules:
        raise HTTPException(status_code=404, detail="Расписания не найдены")
    return schedules

