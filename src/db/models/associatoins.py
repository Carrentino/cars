from helpers.sqlalchemy.base_model import Base
from sqlalchemy import Table, ForeignKey, Column, UUID

car_options_association = Table(
    'car_options_association', Base.metadata,
    Column('car_id', UUID, ForeignKey('cars.id'), primary_key=True),
    Column('car_option_id', UUID, ForeignKey('car_options.id'), primary_key=True)
)
