from datetime import timezone, datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from city.models import City
from dependencies import get_db
from temperature import models
from temperature.crud import fetch_temperature
from temperature.schemas import Temperature


router = APIRouter()

@router.post("/temperatures/update/")
async def update_temperature(db: Session = Depends(get_db)):
    cities = db.query(City).all()

    for city in cities:
        data = await fetch_temperature(city.name)

        temperature = models.Temperature(
            city_id=city.id,
            date_time=datetime.now(timezone.utc),
            temperature=data["current"]["temp_c"]
        )
        db.add(temperature)
    db.commit()

    return {"status": "updated"}
