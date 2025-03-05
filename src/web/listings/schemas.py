from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CarOption(BaseModel):
    title: str


class CreateCarReq(BaseModel):
    car_model_id: UUID
    color: str
    price: int
    latitude: str
    longitude: str
    date_from: datetime | None = None
    date_to: datetime | None = None
    options: list[CarOption]


class CreateCarResp(BaseModel):
    id: UUID
