from datetime import datetime, date

from bson import ObjectId


from openapi_server.apis.default_api_base import BaseDefaultApi
from openapi_server.impl import api_calls
from openapi_server.models.comment import Comment
from openapi_server.models.comment_list_response import CommentListResponse
from motor.motor_asyncio import AsyncIOMotorClient

from openapi_server.models.new_comment import NewComment
from openapi_server.utils.url_creator import generate_url_offset

client = AsyncIOMotorClient("mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")

mongodb = client.get_database("laWikiDB")

# Removes ObjectID fields and converts them to string
pipeline_remove_id = [
    {'$addFields': {"id": {'$toString': '$_id'},
                    "article_id": {'$toString': '$article_id'},
                    "author.id": {'$toString': '$author._id'}
                    }
     },
    {'$unset': ["_id", "author._id"]}  # Remove the original _id fields
]

# Groups all comments in a list
pipeline_group_comments = [
    {"$group": {
        "_id": None,
        "comments": {"$push": "$$ROOT"},
    }},
    {
        "$project": {
            "_id": 0,
        }
    }
]

class ContentManager(BaseDefaultApi):

    async def delete_comment(self, comment_id: str) -> None:
        """Deletes an article's comment"""
        result = await mongodb['comment'].delete_one({"_id": ObjectId(comment_id)})
        if result.deleted_count == 0:
            raise Exception("Comment not found")
        return None

    async def get_article_comments(
            self,
            article_id: str,
            order: str,
            limit: int,
            offset: int,
            creation_date: str,
    ) -> CommentListResponse:
        """Retrieves all comments from an articles"""
        path = "/comments/articles/{article_id}"
        path_vars = {"article_id": article_id}
        return await get_comments_by_parameters(path, path_vars, order, limit, offset, creation_date = creation_date, article_id = article_id)

    async def post_comment(
            self,
            article_id: str,
            new_comment: NewComment,
    ) -> Comment:
        """Post Comment"""
        art_id = ObjectId(article_id)

        if not await api_calls.check_article(article_id):
            raise Exception("Article not found")

        # if not mongodb['article'].find_one({"_id": art_id}):
        #     raise Exception("Article not found")

        today = date.today()

        author_dict = {'id': new_comment.author_id,
                       'name': 'author_name',
                       'image': 'author_image'}
        comment_dic = {
            'article_id': article_id,
            'author': author_dict,
            'body': new_comment.body,

            'creation_date': datetime(today.year, today.month, today.day)
        }
        result = await mongodb['comment'].insert_one(comment_dic)
        if result:
            comment_dic['id'] = str(result.inserted_id)
            return Comment.from_dict(comment_dic)
        else:
            raise Exception("Error creating comment")

    async def get_users_comments(
            self,
            user_id: str,
            article_id: str,
            order: str,
            limit: int,
            offset: int,
            creation_date: str,
    ) -> CommentListResponse:
        """Retrieves all comments from a user"""
        path = "/comments/users/{user_id}"
        path_vars = {"user_id": user_id}
        return await get_comments_by_parameters(path, path_vars, order, limit, offset, creation_date, user_id, article_id)

def parse_date(date_str):
    res_date = datetime.strptime(date_str, "%Y/%m/%d")
    return res_date.replace(hour=0, minute=0, second=0, microsecond=0)

def build_pagination_urls(base_path, path_vars, pagination, offset, total_count, limit):
    next_url = generate_url_offset(base_path, path_vars, pagination, offset + limit) if offset + limit < total_count else None
    prev_url = generate_url_offset(base_path, path_vars, pagination, max(offset - limit, 0)) if offset > 0 else None
    return next_url, prev_url


async def get_comments_by_parameters(path, path_vars, order, limit, offset, creation_date = None, user_id = None, article_id = None):
    """General function to retrieve comments by parameters"""
    pagination = {"limit": limit, "offset": offset} # Dictionary for pagination info in the url
    matching_variables = {} # Dictionary for the filters

    if user_id is not None and path_vars["user_id"] is None: # If the user_id is in the path, we don't need to filter by it
        matching_variables["author._id"] = ObjectId(user_id)
        pagination["user_id"] = user_id
    if article_id is not None and path_vars["article_id"] is None:
        matching_variables["article_id"] = ObjectId(article_id)
        pagination["article_id"] = article_id
    if creation_date is not None:
        dates = creation_date.split("-")
        pagination["creation_date"] = creation_date
        # En funcion de si hay una o dos fechas, se filtra por una o por un rango
        if len(dates) == 1:
            matching_variables["creation_date"] = parse_date(dates[0])
        elif len(dates) == 2:
            matching_variables["creation_date"] = {
                "$gte": parse_date(dates[0]),
                "$lte": parse_date(dates[1])
            }

    total_count = await mongodb['comment'].count_documents(matching_variables) # Contamos el numero de comentarios que cumplen con los filtros
    next_url, prev_url = build_pagination_urls(path, path_vars,
                                               pagination, offset, total_count, limit) # Generamos las urls de paginacion
    query_pipeline = [
        {"$match": matching_variables},
        {"$sort": {"creation_date": -1 if order == "recent" else 1}},
        {"$skip": offset},
        {"$limit": limit},
        *pipeline_remove_id,
        *pipeline_group_comments,
        {"$addFields": {
            "total": total_count,
            "offset": offset,
            "limit": limit,
            "next": next_url,
            "previous": prev_url
            }
        }
    ]

    comments = await mongodb['comment'].aggregate(query_pipeline).to_list(length=1);

    if not comments[0].get('comments'):
        raise Exception("Not found")

    return comments[0]
