from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class UpdateScore(BaseModel):
    car_id: UUID
    score: Decimal
