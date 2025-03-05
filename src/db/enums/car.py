from enum import StrEnum


class CarStatus(StrEnum):
    NOT_VERIFIED = 'NOT_VERIFIED'
    VERIFIED = 'VERIFIED'
    ARCHIVED = 'ARCHIVED'
    BANNED = 'BANNED'
