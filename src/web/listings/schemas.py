from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class CarOption(BaseModel):
    title: str


class CreateCarReq(BaseModel):
    car_model_id: str
    color: str
    price: int
    latitude: str
    longitude: str
    date_from: datetime | None = None
    date_to: datetime | None = None
    options: list[CarOption] = []


class CarResp(BaseModel):
    id: str


class CarFilters(BaseModel):
    car_id: str | None = None
    color: str | None = None
    car_model__title: str | None = None
    brand__title: str | None = None

    price__gte: int | None = None
    price__lte: int | None = None
    score__gte: Decimal | None = None
    score__lte: Decimal | None = None

    date_from__gte: datetime | None = None
    date_from__lte: datetime | None = None
    date_to__gte: datetime | None = None
    date_to__lte: datetime | None = None

    car_model__hp__gte: int | None = None
    car_model__hp__lte: int | None = None
    car_model__engine_capacity__gte: Decimal | None = None
    car_model__engine_capacity__lte: Decimal | None = None
    car_model__fuel_consumption__gte: Decimal | None = None
    car_model__fuel_consumption__lte: Decimal | None = None

    offset: int = 0
    limit: int = 30


class BrandSchema(BaseModel):
    id: UUID
    title: str


class CarModelShortSchema(BaseModel):
    id: UUID
