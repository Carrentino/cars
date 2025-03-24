from enum import StrEnum


class CarModelDrive(StrEnum):
    RWD = 'RWD'
    FWD = 'FWD'
    AWD = 'AWD'


class CarModelGearbox(StrEnum):
    MANUAL = 'Механическая'
    AUTOMATIC = 'Автоматическая'
    ROBOT = 'Робот'
    CVT = 'Вариатор'


class CarModelBody(StrEnum):
    SEDAN = 'Седан'
    LIFTBACK = 'Лифтбек'
    COUPE = 'Купе'
    HATCHBACK_3 = 'Хэтчбек (3 двери)'
    HATCHBACK_5 = 'Хэтчбек (5 дверей)'
    WAGON = 'Универсал'
    SUV_3 = 'Внедорожник (3 двери)'
    SUV_5 = 'Внедорожник (5 дверей)'
    MINIVAN = 'Минивэн'
    PICKUP = 'Пикап'
    LIMOUSINE = 'Лимузин'
    VAN = 'Фургон'
    CABRIOLET = 'Кабриолет'


class CarModelFuel(StrEnum):
    AI_92 = 'АИ-92'
    AI_95 = 'АИ-95'
    AI_100 = 'АИ-100'
    GAS = 'Газ'
    DIESEL = 'Дизельное топливо'
    ELECTRO = 'Электро'
