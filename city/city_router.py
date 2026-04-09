from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from city.schemas import City, CityCreate
from city import crud
from dependencies import get_db

router = APIRouter()


@router.post("/cities/", response_model=City)
def create_city(city: CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(city=city, db=db)


@router.get("/cities/", response_model=list[City])
def get_cities(db: Session = Depends(get_db)):
    return crud.get_cities(db=db)
