from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

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
    #check patient
    patient = (
    db.query(models.Patient)
    .filter(models.Patient.id == appointment.patient_id)
    .first()
)

    if not patient:
        raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )
    #Check Doctor    
    doctor = (
    db.query(models.Doctor)
    .filter(models.Doctor.id == appointment.doctor_id)
    .first()
)

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
    )
    existing_appointment = (
    db.query(models.Appointment)
    .filter(
        models.Appointment.doctor_id == appointment.doctor_id,
        models.Appointment.appointment_date == appointment.appointment_date,
        models.Appointment.appointment_time == appointment.appointment_time
    )
    .first()
)

    if existing_appointment:
        raise HTTPException(
            status_code=400,
            detail="This appointment slot is already booked."
    )
        
    schedule = (
    db.query(models.DoctorSchedule)
    .filter(
        models.DoctorSchedule.doctor_id == appointment.doctor_id,
        models.DoctorSchedule.date == appointment.appointment_date
    )
    .first()
)

    if not schedule:
        raise HTTPException(
            status_code=400,
            detail="Doctor is not available on this date."
    )
    if (
    appointment.appointment_time < schedule.start_time
    or
    appointment.appointment_time > schedule.end_time
):
        raise HTTPException(
        status_code=400,
        detail="Appointment time is outside the doctor's working hours."
    )   
    db_appointment = models.Appointment(**appointment.model_dump())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment
#crud get appointment
def get_appointment(db: Session):
    return db.query(models.Appointment).all()

#CANCEL APPOINTMENT
def cancel_appointment(db: Session, appointment_id: int):

    appointment = (
        db.query(models.Appointment)
        .filter(models.Appointment.id == appointment_id)
        .first()
    )

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    if appointment.status == "Cancelled":
        raise HTTPException(
            status_code=400,
            detail="Appointment is already cancelled"
        )

    appointment.status = "Cancelled"

    db.commit()
    db.refresh(appointment)

    return appointment

def reschedule_appointment(
    db: Session,
    appointment_id: int,
    new_data: schemas.AppointmentReschedule
):
    appointment = (
    db.query(models.Appointment)
    .filter(models.Appointment.id == appointment_id)
    .first()
)

    if not appointment:
        raise HTTPException(
        status_code=404,
        detail="Appointment not found"
    )
    if appointment.status == "Cancelled":
        raise HTTPException(
        status_code=400,
        detail="Cancelled appointments cannot be rescheduled."
    )
        
    schedule = (
    db.query(models.DoctorSchedule)
    .filter(
        models.DoctorSchedule.doctor_id == appointment.doctor_id,
        models.DoctorSchedule.date == new_data.appointment_date
    )
    .first()
)

    if not schedule:
        raise HTTPException(
        status_code=400,
        detail="Doctor is not available on this date."
    )
    
    if (
    new_data.appointment_time < schedule.start_time
    or
    new_data.appointment_time > schedule.end_time
):
        raise HTTPException(
        status_code=400,
        detail="Appointment time is outside the doctor's working hours."
    )
    existing_appointment = (
    db.query(models.Appointment)
    .filter(
        models.Appointment.doctor_id == appointment.doctor_id,
        models.Appointment.appointment_date == new_data.appointment_date,
        models.Appointment.appointment_time == new_data.appointment_time,
        models.Appointment.id != appointment_id
    )
    .first()
)

    if existing_appointment:
        raise HTTPException(
        status_code=400,
        detail="This appointment slot is already booked."
    )
    appointment.appointment_date = new_data.appointment_date
    appointment.appointment_time = new_data.appointment_time

    db.commit()
    db.refresh(appointment)

    return appointment