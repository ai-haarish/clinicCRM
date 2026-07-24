from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, Boolean
from .database import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=False)
    experience = Column(Integer)
    consultation_fee = Column(Integer)


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(15), unique=True)
    age = Column(Integer)
    gender = Column(String(10))
    
class DoctorSchedule(Base):
    __tablename__ = "doctor_schedule"
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    is_available = Column(Boolean, default=True)
    
class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    appointment_date = Column(Date)
    appointment_time = Column(Time)
    status = Column(String(30), default="Scheduled")