from fastapi import HTTPException
from traceback import format_exc


MESSAGE_UNEXPECTED = "Unexpected server error"
MESSAGE_BAD_FORMAT = "Malformed request, check ID formatting or other fields"
MESSAGE_NOT_FOUND = "{resource} not found"
MESSAGE_NOT_FOUND_NESTED = "Server error, may be caused by invalid properties such as invalid ID"
MESSAGE_UNAKCNOWLEDGED = "Request for operation was unacknowledged"
MESSAGE_NAME_WHEN_ID = "Argument must be a valid ID, cannot be name"
MESSAGE_CANT_RETURN = "Cannot return content currently, operation processed"
MESSAGE_CANT_TRANSLATE = "Failed to translate wiki, update succesful"
MESSAGE_FORBIDDEN = "Forbidden operation, check user permissions"

HTTP_REQUEST_FORMAT = "http://{url}/{method}"
REMOVE_ALL_ARTICLES = "v2/articles/wiki/{id}"
REMOVE_ALL_TAGS = "v2/tags/wikis/{id}"
GET_USER_BY_ID = "v1/users/{id}"

SUPPORTED_LANGUAGES = ["en", "es", "fr"]

def raise_http_exception(code : int, message : str, e: Exception):
    print(e)
    print(type(e))
    print(format_exc())
    raise HTTPException(status_code=code, detail=message + '. More details: ' + str(e))