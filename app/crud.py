from sqlalchemy.orm import Session
from . import models, schemas


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