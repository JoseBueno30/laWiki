from typing import Any, Dict


def generate_url(path: str, path_var : Any, query_var : Dict[str,Any]):
    """
    Generate the url for the request
    """
    url = path
    if path_var:
        url = url.format(**path_var)
    if query_var:
        url += "?"
        for key, value in query_var.items():
            url += f"{key}={value}&"
        url = url[:-1]
    return url

def generate_url_offset(path: str, path_var : Any, query_var : Dict[str,Any], offset: int):
    """
    Generate the url for the request with offset
    """
    query_var["offset"] = offset # This is wrong, because it updates the original query_var reference
    return generate_url(path, path_var, query_var)