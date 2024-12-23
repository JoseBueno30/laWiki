from datetime import datetime, date

from bson import ObjectId
from fastapi import HTTPException

from openapi_server.apis.v2.v2_public_api_base import BaseV2PublicApi
from openapi_server.impl import api_calls
from openapi_server.models.comment import Comment
from openapi_server.models.comment_list_response import CommentListResponse
from motor.motor_asyncio import AsyncIOMotorClient

from openapi_server.models.new_comment import NewComment
from ..operations import parse_date, build_pagination_urls
from ..pipelines import pipeline_remove_id, pipeline_trunc_date, pipeline_group_comments

client = AsyncIOMotorClient("mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")
mongodb = client.get_database("laWikiV2BD")


class V2PublicComments(BaseV2PublicApi):
    async def v2_delete_comment(
            self,
            comment_id: str,
            user_id: str,
            admin: bool,
    ) -> None:
        """Deletes an article's comment"""
        try:
            comment_oid = ObjectId(comment_id)
        except:
            raise HTTPException(status_code=400, detail="Bad Request, invalid Comment ID format")

        comment = await mongodb['comment'].find_one({"_id": comment_oid})
        if comment is None:
            raise HTTPException(status_code=404, detail="Comment not found")

        # If the user is not an admin, we check if the user is the author of the comment
        if not admin and comment['author']['_id'] != ObjectId(user_id):
            raise HTTPException(status_code=403, detail="Forbidden")

        await mongodb['comment'].delete_one({"_id": ObjectId(comment_id)})
        return None

    async def v2_post_comment(
            self,
            article_id: str,
            user_id: str,
            admin: bool,
            new_comment: NewComment,
    ) -> Comment:
        if not await api_calls.check_article(article_id):
            raise HTTPException(status_code=404, detail="Article not found")

        # As the get method is restricted, I pass the same headers to the get_user method
        # If the client is authorized to get the user, it will be authorized to post the comment
        author = await api_calls.get_user(new_comment.author_id, user_id, admin)

        today = datetime.today()

        author_dict = {'_id': ObjectId(new_comment.author_id),
                       'name': author['username'],
                       'image': author['image']}
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
            raise HTTPException(status_code=400, detail="Bad Request, wrong content structure")

    async def v2_get_articles_comments(
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
        return await get_comments_by_parameters(path, path_vars, order, limit, offset, creation_date, None,
                                                article_id)

    async def v2_get_users_comments(
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


async def get_comments_by_parameters(path, path_vars, order, limit, offset, creation_date=None, user_id=None,
                                     article_id=None):
    """General function to retrieve comments by parameters"""
    res_query_params = {"limit": limit, "offset": offset}  # Dictionary for pagination info in the url
    matching_variables = {}  # Dictionary for the filters

    if user_id is not None:
        matching_variables["author._id"] = ObjectId(user_id)
        if "user_id" not in path_vars:  # Path variables don´t need to be added to the query url
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

    total_count = await mongodb['comment'].count_documents(
        matching_variables)  # Contamos el numero de comentarios que cumplen con los filtros
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
    comments = await mongodb['comment'].aggregate(query_pipeline).to_list(length=1)

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
