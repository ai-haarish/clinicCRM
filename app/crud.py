from sqlalchemy.orm import Session
from . import models, schemas

#crud create doctor
def create_doctor(db: Session, doctor: schemas.DoctorCreate):
    db_doctor = models.Doctor(
        name=doctor.name,
        specialization=doctor.specialization,
        experience=doctor.experience,
        consultation_fee=doctor.consultation_fee,
    )

    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)

    return db_doctor

#crud get doctor
def get_doctors(db):
    return db.query(models.Doctor).all()

#crud create doctor schedule
def create_schedule(db: Session, schedule: schemas.DoctorScheduleCreate):

    db_schedule = models.DoctorSchedule(**schedule.model_dump())

    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)

    return db_schedule

#crud get doctor schedule
def get_schedules(db: Session):
    return db.query(models.DoctorSchedule).all()

#crud create patient
def create_patient(db: Session, patient: schemas.PatientCreate):
    db_patient = models.Patient(**patient.model_dump())

    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)

    return db_patient

#crud get patient
def get_patients(db: Session):
    return db.query(models.Patient).all()

#crud create appointment
def create_appointment(db: Session, appointment: schemas.AppointmentCreate):
    db_appointment = models.Appointment(**appointment.model_dump())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment
#crud get appointment
def get_appointment(db: Session):
    return db.query(models.Appointment).all()