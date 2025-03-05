from helpers.errors import ServerError
from starlette import status


class UserIsNotVerifiedHttpError(ServerError):
    status_code = status.HTTP_403_FORBIDDEN
    message = 'User is not verified'
