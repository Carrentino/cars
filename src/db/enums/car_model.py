from enum import StrEnum


class CarModelDrive(StrEnum):
    RWD = 'RWD'
    FWD = 'FWD'
    AWD = 'AWD'


class CarModelGearbox(StrEnum):
    MANUAL = 'MANUAL'
    AUTOMATIC = 'AUTOMATIC'
    ROBOT = 'ROBOT'
    CVT = 'CVT'


class CarModelBody(StrEnum):
    SEDAN = 'SEDAN'
    LIFTBACK = 'LIFTBACK'
    COUPE = 'COUPE'
    HATCHBACK_3 = 'HATCHBACK_3'
    HATCHBACK_5 = 'HATCHBACK_5'
    WAGON = 'WAGON'
    SUV_3 = 'SUV_3'
    SUV_5 = 'SUV_5'
    MINIVAN = 'MINIVAN'
    PICKUP = 'PICKUP'
    LIMOUSINE = 'LIMOUSINE'
    VAN = 'VAN'
    CABRIOLET = 'CABRIOLET'


class CarModelFuel(StrEnum):
    AI_92 = 'AI_92'
    AI_95 = 'AI_95'
    AI_100 = 'AI_100'
    GAS = 'GAS'
    DIESEL = 'DIESEL'
    ELECTRO = 'ELECTRO'
