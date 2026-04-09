from datetime import timezone, datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from city.models import City
from city.crud import get_city
from dependencies import get_db
from temperature import models
from temperature import crud
from temperature.schemas import Temperature


router = APIRouter()

@router.post("/temperatures/update/")
async def update_temperature(db: Session = Depends(get_db)):
    cities = db.query(City).all()

    for city in cities:
        data = await crud.fetch_temperature(city.name)

        temperature = models.Temperature(
            city_id=city.id,
            date_time=datetime.now(timezone.utc),
            temperature=data["current"]["temp_c"]
        )
        db.add(temperature)
    db.commit()

    return {"status": "updated"}


@router.get("/temperatures/", response_model=list[Temperature])
def get_temperature_list(db: Session = Depends(get_db)):
    return crud.get_temperature_list(db)


@router.get("/temperatures/{city_id}/", response_model=list[Temperature])
def get_temperature_by_city_id(city_id: int, db: Session = Depends(get_db)):
    city = get_city(city_id=city_id, db=db)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return crud.get_city_temperature(city_id=city.id, db=db)
