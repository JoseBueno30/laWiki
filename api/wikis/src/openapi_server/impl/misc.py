from fastapi import HTTPException


MESSAGE_UNEXPECTED = "Unexpected server error"
MESSAGE_BAD_FORMAT = "Malformed request, check ID formatting or other fields"
MESSAGE_NOT_FOUND = "{resource} not found"
MESSAGE_NOT_FOUND_NESTED = "Server error, may be caused by invalid properties such as invalid ID"

def raise_http_exception(code : int, message : str, e: Exception):
    print(e)
    print(type(e))
    raise HTTPException(status_code=code, detail=message)