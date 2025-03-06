from helpers.errors import ServerError
from starlette import status


class UserIsNotVerifiedHttpError(ServerError):
    status_code = status.HTTP_403_FORBIDDEN
    message = 'User is not verified'


class CarNotFoundHttpError(ServerError):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'Car not found'


class CarModelNotFoundHttpError(ServerError):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'Car Model not found'


class UserIsNotOwnerHttpError(ServerError):
    status_code = status.HTTP_403_FORBIDDEN
    message = 'User is not owner'
