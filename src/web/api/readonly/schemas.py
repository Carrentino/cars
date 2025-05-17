from datetime import datetime
from decimal import Decimal
from uuid import UUID

from helpers.models.response import PaginatedResponse
from pydantic import BaseModel

from src.db.enums.car_model import CarModelBody, CarModelDrive, CarModelGearbox, CarModelFuel
from src.web.api.listings.schemas import BrandSchema


class BrandPaginatedResponse(PaginatedResponse):
    data: list[BrandSchema]


class CarModelShortSchema(BaseModel):
    id: UUID
    title: str
    body: CarModelBody
    fuel_consumption: Decimal
    engine_capacity: Decimal
    drive: CarModelDrive
    gearbox: CarModelGearbox
    fuel: CarModelFuel
    hp: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CarModelPaginatedResponse(PaginatedResponse):
    data: list[CarModelShortSchema]
