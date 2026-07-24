from pydantic import BaseModel
from datetime import date, time


class DoctorCreate(BaseModel):
    name: str
    specialization: str
    experience: int
    consultation_fee: int


class DoctorResponse(DoctorCreate):
    id: int

    class Config:
        from_attributes = True

class DoctorScheduleCreate(BaseModel):
    doctor_id: int
    date: date
    start_time: time
    end_time: time
    is_available: bool

class DoctorScheduleResponse(DoctorScheduleCreate):
    id: int

    class Config:
        from_attributes = True
        
class PatientCreate(BaseModel):
    name: str
    phone: str
    age: int
    gender: str


class PatientResponse(PatientCreate):
    id: int

    class Config:
        from_attributes = True
    
class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time
    status: str
    
class AppointmentResponse(AppointmentCreate):
    id: int
    class Config:
        from_attributes = True