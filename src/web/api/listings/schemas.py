from datetime import datetime
from decimal import Decimal
from uuid import UUID

from fastapi.params import Query
from helpers.models.response import PaginatedResponse
from pydantic import BaseModel, Field

from src.db.enums.car import CarStatus
from src.db.enums.car_model import CarModelFuel, CarModelGearbox, CarModelDrive, CarModelBody


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
    car__id: list[UUID] | None = Field(Query(None))
    car__color: list[str] | None = Field(Query(None))
    car_model__title: list[str] | None = Field(Query(None))
    brand__title: list[str] | None = Field(Query(None))

    car__price__gte: int | None = None
    car__price__lte: int | None = None
    car__score__gte: Decimal | None = None
    car__score__lte: Decimal | None = None

    car__date_from__gte: datetime | None = None
    car__date_from__lte: datetime | None = None
    car__date_to__gte: datetime | None = None
    car__date_to__lte: datetime | None = None

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
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CarModelSchema(BaseModel):
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
    brand: BrandSchema

    class Config:
        from_attributes = True


class CarSchema(BaseModel):
    id: UUID
    color: str
    score: Decimal
    price: int
    owner_id: UUID
    latitude: str
    longitude: str
    date_from: datetime | None
    date_to: datetime | None
    status: CarStatus
    created_at: datetime
    updated_at: datetime
    car_model: CarModelSchema

    class Config:
        from_attributes = True


class CarPaginatedResponse(PaginatedResponse):
    data: list[CarSchema]


class CarAttachmentSchema(BaseModel):
    id: UUID
    attachment: str

    class Config:
        from_attributes = True


class CarOptionSchema(BaseModel):
    id: UUID
    title: str

    class Config:
        from_attributes = True


class RetrieveCarSchema(CarSchema):
    attachments: list[CarAttachmentSchema]
    options: list[CarOptionSchema]
    reviews: list

    class Config:
        from_attributes = True


class UpdateCarSchema(BaseModel):
    color: str
    price: int
    latitude: str
    longitude: str
    date_from: datetime | None = None
    date_to: datetime | None = None
    options: list[CarOption]


class DeleteAttachmentElementSchema(BaseModel):
    id: UUID


class DeleteAttachmentsSchema(BaseModel):
    attachments: list[DeleteAttachmentElementSchema]
