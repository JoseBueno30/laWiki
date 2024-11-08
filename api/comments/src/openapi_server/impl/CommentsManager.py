from datetime import datetime, date

from bson import ObjectId
from dns.e164 import query

from openapi_server.apis.default_api_base import BaseDefaultApi
from openapi_server.models.comment import Comment
from openapi_server.models.comment_list_response import CommentListResponse
from motor.motor_asyncio import AsyncIOMotorClient

from openapi_server.models.new_comment import NewComment
from openapi_server.utils.parsers import from_cursor_to_comment

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

        matching_variables = {}
        if article_id is not None:
            article_id = ObjectId(article_id)
            matching_variables["article_id"] = article_id
        if creation_date is not None:
            print(creation_date)
            dates = creation_date.split("-")
            if len(dates) == 1:
                matching_variables["creation_date"] = datetime.strptime(dates[0], "%Y/%m/%d")
            elif len(dates) == 2:
                matching_variables["creation_date"] = {
                    "$gte": datetime.strptime(dates[0], "%Y/%m/%d"),
                    "$lte": datetime.strptime(dates[1], "%Y/%m/%d")
                }

        print(matching_variables)

        total_count = await mongodb['comment'].count_documents(matching_variables)
        query_pipeline = [
            {"$match": matching_variables},
            {"$sort": {"creation_date": -1 if order == "recent" else 1}},
            {"$skip": offset * limit},
            {"$limit": limit},
            *pipeline_remove_id,
            {"$group": {
                "_id": None,
                "comments": {"$push": "$$ROOT"},
            }},
            {
                "$project": {
                    "_id": 0,
                }
            },
            {"$addFields": {
                "total": total_count,
                "offset": offset,
                "limit": limit,
                "next": {
                    "$cond": {
                        "if" : {"$lt": [limit + offset, total_count]},
                        "then": f"comments/articles/{article_id}?limit={limit}&offset={offset + limit}",
                        "else": None
                    }
                },
                "previous": {
                    "$cond": {
                        "if": {"$gt": [offset, 0]},
                        "then": f"comments/articles/{article_id}?limit={limit}&offset={max(offset - limit, 0)}",
                        "else": None
                    }
                }
            }}
        ]

        comments = await mongodb['comment'].aggregate(query_pipeline).to_list(length=1);

        if not comments[0].get('comments'):
            raise Exception("Not found")

        return comments[0]

    async def post_comment(
            self,
            article_id: str,
            new_comment: NewComment,
    ) -> Comment:
        """Post Comment"""
        art_id = ObjectId(article_id)
        if not mongodb['article'].find_one({"_id": art_id}):
            raise Exception("Article not found")

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

        matching_variables = {"author._id": ObjectId(user_id)}
        if article_id is not None:
            matching_variables["article_id"] = ObjectId(article_id)
        if creation_date is not None:
            dates = creation_date.split("-")
            if len(dates) == 1:
                matching_variables["creation_date"] = datetime.strptime(dates[0], "%Y/%m/%d")
            elif len(dates) == 2:
                matching_variables["creation_date"] = {
                    "$gte": datetime.strptime(dates[0], "%Y/%m/%d"),
                    "$lte": datetime.strptime(dates[1], "%Y/%m/%d")
                }

        total_counts = await mongodb['comment'].count_documents(matching_variables)

        query_pipeline = [
            {"$match": matching_variables},
            {"$sort": {"creation_date": -1 if order == "recent" else 1}},
            {"$skip": offset * limit},
            {"$limit": limit},
            *pipeline_remove_id,
            {"$group": {
                "_id": None,
                "comments": {"$push": "$$ROOT"},
            }},
            {
                "$project": {
                    "_id": 0,
                }
            },
            {"$addFields": {
                "total": total_counts,
                "offset": offset,
                "limit": limit,
                "next": {
                    "$cond": {
                        "if": {"$lt": [limit + offset, total_counts]},
                        "then": f"/comments/users/{user_id}?limit={limit}&offset={offset + limit}",
                        "else": None
                    }
                },
                "previous": {
                    "$cond": {
                        "if": {"$gt": [offset, 0]},
                        "then": f"/comments/users/{user_id}comments?limit={limit}&offset={max(offset - limit, 0)}",
                        "else": None
                    }
                }
            }}
        ]

        comments = await mongodb['comment'].aggregate(query_pipeline).to_list(length=1);

        if not comments[0].get('comments'):
            raise Exception("Not found")

        return comments[0]
