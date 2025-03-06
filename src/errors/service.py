from helpers.errors import BaseError


class UserIsNotVerifiedError(BaseError):
    message = 'User is not verified'


class CarNotFoundError(BaseError):
    message = 'Car not found'


class CarModelNotFoundError(BaseError):
    message = 'Car Model not found'


class UserIsNotOwnerError(BaseError):
    message = 'User is not owner'
