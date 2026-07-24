from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import engine, get_db
from . import models, schemas, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Clinic CRM API")


@app.get("/")
def home():
    return {"message": "Clinic CRM Running 🚀"}

#post doctors
@app.post("/doctors", response_model=schemas.DoctorResponse)
def create_doctor(
    doctor: schemas.DoctorCreate,
    db: Session = Depends(get_db)
):
    return crud.create_doctor(db, doctor)

#get doctors
@app.get("/doctors", response_model=list[schemas.DoctorResponse])
def get_doctors(
    db: Session = Depends(get_db)
):
    return crud.get_doctors(db)

#post schedule of doctor
@app.post("/schedule", response_model=schemas.DoctorScheduleResponse)
def create_schedule(
    schedule: schemas.DoctorScheduleCreate,
    db: Session = Depends(get_db)
):
    return crud.create_schedule(db, schedule)


@app.get("/schedule", response_model=list[schemas.DoctorScheduleResponse])
def get_schedule(
    db: Session = Depends(get_db)
):
    return crud.get_schedules(db)

#PATIENT API
@app.post("/patients", response_model=schemas.PatientResponse)
def create_patient(
    patient: schemas.PatientCreate,
    db: Session = Depends(get_db)
):
    return crud.create_patient(db, patient)

@app.get("/patients", response_model=list[schemas.PatientResponse])
def get_patients(
    db: Session = Depends(get_db)
):
    return crud.get_patients(db)

#APPOINTMENT API
@app.post("/appointments", response_model=schemas.AppointmentCreate)
def create_appointment(
    appointment: schemas.AppointmentCreate,
    db: Session = Depends(get_db)
):
    return crud.create_appointment(db, appointment)

@app.get("/appointments", response_model=list[schemas.AppointmentResponse])
def get_appointments(
    db: Session = Depends(get_db)
):
    return crud.get_appointment(db)