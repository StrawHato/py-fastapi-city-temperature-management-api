from sqlalchemy.orm import Session

from city import models
from city.schemas import CityCreate


def create_city(db: Session, city: CityCreate):
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session):
    return db.query(models.City).all()


def get_city(db: Session, city_id: int):
    return db.query(models.City).get(city_id)
