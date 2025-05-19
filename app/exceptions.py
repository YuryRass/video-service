"""Различные HTTP-ошибки"""

from fastapi import HTTPException, status


class TokenNotCorrect(Exception):
    detail = "Token is not correct"


class MainAppException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class EmailIsAllredyExist(MainAppException):
    status_code = status.HTTP_409_CONFLICT
    detail = "E-mail is allready exist"


class UserUnauthorizedException(MainAppException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User is unauthorized"


class IncorrectJWTtokenException(MainAppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "JWT token is incorrect"


class JWTtokenExpiredException(MainAppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "JWT token is expired"


class UserIsNotPresentException(MainAppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = ""


class UserIsAllredyRegistered(MainAppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "User is allready registered"


class IncorrectEmailOrPasswordException(MainAppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect e-mail or password"
