from fastapi import HTTPException


class ErrorResponse:
    @staticmethod
    def error(message: str, status_code: any):
        return HTTPException(status_code=status_code, detail=message)
