from enum import StrEnum


class CarStatus(StrEnum):
    NOT_VERIFIED = 'Не верифицировано'
    VERIFIED = 'Верифицировано'
    ARCHIVED = 'Архивно'
    BANNED = 'Заблокировано'
