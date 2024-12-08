from datetime import datetime, date
from xml.dom import NotFoundErr

from bson import ObjectId

from openapi_server.apis.default_api_base import BaseDefaultApi
from openapi_server.impl import api_calls
from openapi_server.models.comment import Comment
from openapi_server.models.comment_list_response import CommentListResponse
from motor.motor_asyncio import AsyncIOMotorClient

from openapi_server.models.new_comment import NewComment
from openapi_server.utils.url_creator import generate_url_offset

client = AsyncIOMotorClient("mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")
mongodb = client.get_database("laWikiV2BD")

# Removes ObjectID fields and converts them to string
pipeline_remove_id = [
    {'$addFields': {"id": {'$toString': '$_id'},
                    "article_id": {'$toString': '$article_id'},
                    "author.id": {'$toString': '$author._id'}
                    }
     },
    {'$unset': ["_id", "author._id"]}  # Remove the original _id fields
]

pipeline_trunc_date = [
    {
        "$set": {
            "creation_date": {
                "$dateFromParts": {
                    "year": {"$year": "$creation_date"},
                    "month": {"$month": "$creation_date"},
                    "day": {"$dayOfMonth": "$creation_date"}
                }
            }
        }
    }
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


class DefaultCommentsManager(BaseDefaultApi):

    async def delete_comment(self, comment_id: str) -> None:
        """Deletes an article's comment"""
        result = await mongodb['comment'].delete_one({"_id": ObjectId(comment_id)})
        if result.deleted_count == 0:
            raise NotFoundErr("Comment not found")
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
        return await get_comments_by_parameters(path, path_vars, order, limit, offset, creation_date, None, article_id)

    async def post_comment(
            self,
            article_id: str,
            new_comment: NewComment,
    ) -> Comment:
        """Post Comment"""

        if not await api_calls.check_article(article_id):
            raise NotFoundErr("Article not found")

        # if not mongodb['article'].find_one({"_id": art_id}):
        #     raise Exception("Article not found")

        today = datetime.today()
        print(today)

        author_dict = {'_id': ObjectId(new_comment.author_id),
                       'name': 'author_name',
                       'image': 'author_image'}
        comment_dic = {
            'article_id': ObjectId(article_id),
            'author': author_dict,
            'body': new_comment.body,

            'creation_date': today
        }
        result = await mongodb['comment'].insert_one(comment_dic)
        if result:
            # Once inserted, we return the comment with the id as strings
            comment_dic['id'] = str(result.inserted_id)
            comment_dic['article_id'] = str(comment_dic['article_id'])
            comment_dic['author']['id'] = str(comment_dic['author']['_id'])
            comment_dic['creation_date'] = date(today.year, today.month, today.day)
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
        return await get_comments_by_parameters(path, path_vars, order, limit, offset, creation_date, user_id,
                                                article_id)


def parse_date(date_str):
    res_date = datetime.strptime(date_str, "%Y/%m/%d")
    return res_date.replace(hour=0, minute=0, second=0, microsecond=0)


def build_pagination_urls(base_path, path_vars, pagination, offset, total_count, limit):
    next_url = generate_url_offset(base_path, path_vars, pagination,
                                   offset + limit) if offset + limit < total_count else None
    prev_url = generate_url_offset(base_path, path_vars, pagination, max(offset - limit, 0)) if offset > 0 else None
    return next_url, prev_url


async def get_comments_by_parameters(path, path_vars, order, limit, offset, creation_date=None, user_id=None,
                                     article_id=None):
    """General function to retrieve comments by parameters"""
    res_query_params = {"limit": limit, "offset": offset}  # Dictionary for pagination info in the url
    matching_variables = {}  # Dictionary for the filters

    if user_id is not None:
        matching_variables["author._id"] = ObjectId(user_id)
        if "user_id" not in path_vars:  # Path variables dont need to be added to the query url
            res_query_params["user_id"] = user_id
    if article_id is not None:
        matching_variables["article_id"] = ObjectId(article_id)
        if "article_id" not in path_vars:
            res_query_params["article_id"] = article_id
    if creation_date is not None:
        dates = creation_date.split("-")
        res_query_params["creation_date"] = creation_date
        # En funcion de si hay una o dos fechas, se filtra por una o por un rango
        if len(dates) == 1:
            matching_variables["creation_date"] = parse_date(dates[0])
        elif len(dates) == 2:
            matching_variables["creation_date"] = {
                "$gte": parse_date(dates[0]),
                "$lte": parse_date(dates[1])
            }

    total_count = await mongodb['comment'].count_documents(matching_variables)  # Contamos el numero de comentarios que cumplen con los filtros
    next_url, prev_url = build_pagination_urls(path, path_vars,
                                               res_query_params, offset, total_count,
                                               limit)  # Generamos las urls de paginacion
    query_pipeline = [
        {"$match": matching_variables},
        {"$sort": {"creation_date": -1 if order == "recent" else 1, "body": 1}},
        {"$skip": offset},
        {"$limit": limit},
        *pipeline_remove_id,
        *pipeline_trunc_date,
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

    if not comments:
        comments.append({
            "comments": [],
            "total": total_count,
            "offset": offset,
            "limit": limit,
            "next": next_url,
            "previous": prev_url
        })

    return comments[0]
