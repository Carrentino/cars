from helpers.errors import BaseError


class UserIsNotVerifiedError(BaseError):
    message = 'User is not verified'
