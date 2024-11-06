from datetime import datetime
from typing import Dict

from openapi_server.models.author import Author
from openapi_server.models.comment import Comment
from openapi_server.models.comment_list_response import CommentListResponse

def from_cursor_to_comment(doc: Dict) -> Comment:
    return Comment(
        id=doc['id'],
        article_id=doc['art_id'],
        author=from_cursor_to_author(doc['author']),
        body=doc['body'],
        creation_date= doc['creation_date'].strftime("%Y-%m-%d")
    )

def from_cursor_to_author(doc: Dict) -> Author:
    return Author(
        id=doc['id'],
        name=doc['name'],
        image=doc['image']
    )
