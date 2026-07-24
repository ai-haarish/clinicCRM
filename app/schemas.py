from pydantic import BaseModel


class DoctorCreate(BaseModel):
    name: str
    specialization: str
    experience: int
    consultation_fee: int


class DoctorResponse(DoctorCreate):
    id: int

    class Config:
        from_attributes = True