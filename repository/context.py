from fastapi.requests import Request


def context( request:Request, data:dict = {}):
     data.update({"request":request})
     return data
     