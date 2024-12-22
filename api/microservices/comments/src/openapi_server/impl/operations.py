from datetime import datetime

from openapi_server.utils.url_creator import generate_url_offset

def parse_date(date_str):
    res_date = datetime.strptime(date_str, "%Y/%m/%d")
    return res_date.replace(hour=0, minute=0, second=0, microsecond=0)


def build_pagination_urls(base_path, path_vars, pagination, offset, total_count, limit):
    next_url = generate_url_offset(base_path, path_vars, pagination,
                                   offset + limit) if offset + limit < total_count else None
    prev_url = generate_url_offset(base_path, path_vars, pagination, max(offset - limit, 0)) if offset > 0 else None
    return next_url, prev_url