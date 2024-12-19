# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.v2_public_api_base import BaseV2PublicApi
import openapi_server.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from datetime import date
from pydantic import Field, StrictBool, StrictInt, StrictStr
from typing import Any, List, Optional
from typing_extensions import Annotated
from openapi_server.models.article import Article
from openapi_server.models.article_list import ArticleList
from openapi_server.models.article_version import ArticleVersion
from openapi_server.models.article_version_body import ArticleVersionBody
from openapi_server.models.article_version_list import ArticleVersionList
from openapi_server.models.average_rating import AverageRating
from openapi_server.models.comment import Comment
from openapi_server.models.comment_list_response import CommentListResponse
from openapi_server.models.new_comment import NewComment
from openapi_server.models.new_rating import NewRating
from openapi_server.models.rating import Rating
from openapi_server.models.tag import Tag
from openapi_server.models.tag_list import TagList
from openapi_server.models.wiki import Wiki
from openapi_server.models.wiki_list import WikiList
from openapi_server.security_api import get_token_oauth_token

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.delete(
    "/v2/comments/{comment_id}",
    responses={
        204: {"description": "No Content, comment deleted successfully"},
        400: {"description": "Bad Request, invalid Comment ID format"},
        403: {"description": "Forbidden"},
        404: {"description": "Comment not found"},
    },
    tags=["v2/public"],
    summary="Delete Comment",
    response_model_by_alias=True,
)
async def delete_comment_v2(
    comment_id: Annotated[StrictStr, Field(description="The unique ID of the article")] = Path(..., description="The unique ID of the article"),
    token_oauth_token: TokenModel = Security(
        get_token_oauth_token
    ),
) -> None:
    """Deletes an article&#39;s comment"""
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2PublicApi.subclasses[0]().delete_comment_v2(comment_id)


@router.delete(
    "/v2/ratings/{id}",
    responses={
        204: {"description": "Deleted successfully"},
        400: {"description": "Bad Request, invalid Rating ID format"},
        403: {"description": "No permissions to delete"},
        404: {"description": "Rating Not Found"},
    },
    tags=["v2/public"],
    summary="Delete Rating",
    response_model_by_alias=True,
)
async def delete_rating_v2(
    id: StrictStr = Path(..., description=""),
) -> None:
    """Delete the rating associated with the selected ID"""
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2PublicApi.subclasses[0]().delete_rating_v2(id)


@router.put(
    "/v2/ratings/articles/{id}",
    responses={
        201: {"model": Rating, "description": "Rating edited"},
        400: {"description": "Bad Request, invalid Article ID format"},
        403: {"description": "Forbidden"},
        404: {"description": "Not Found"},
    },
    tags=["v2/public"],
    summary="Edit Article&#39;s Rating",
    response_model_by_alias=True,
)
async def edit_article_rating_v2(
    id: StrictStr = Path(..., description=""),
    new_rating: Optional[NewRating] = Body(None, description=""),
) -> Rating:
    """Update the value of an already existing Rating"""
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2PublicApi.subclasses[0]().edit_article_rating_v2(id, new_rating)


@router.get(
    "/v2/ratings/articles/{id}/average",
    responses={
        200: {"model": AverageRating, "description": "OK"},
        400: {"description": "Bad Request, invalid Article ID format"},
    },
    tags=["v2/public"],
    summary="Get Article&#39;s average rating",
    response_model_by_alias=True,
)
async def get_article_average_rating_v2(
    id: StrictStr = Path(..., description=""),
) -> AverageRating:
    """Get data about the average rating of the article"""
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2PublicApi.subclasses[0]().get_article_average_rating_v2(id)


@router.get(
    "/v2/articles/author/{id}",
    responses={
        200: {"model": ArticleList, "description": "OK"},
        400: {"description": "Bad Request, The given ID was not correct."},
        404: {"description": "Author Not Found."},
    },
    tags=["v2/public"],
    summary="Get Articles by Author",
    response_model_by_alias=True,
)
async def get_article_by_author_v2(
    id: StrictStr = Path(..., description=""),
    offset: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")] = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset", ge=0),
    limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="The maximum number of results to return.")] = Query(0, description="The maximum number of results to return.", alias="limit", ge=0, le=100),
    order: Annotated[Optional[StrictStr], Field(description="Sorts the articles by different criteria")] = Query(None, description="Sorts the articles by different criteria", alias="order"),
) -> ArticleList:
    """Get a list of Articles given an author&#39;s ID.  """
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2PublicApi.subclasses[0]().get_article_by_author_v2(id, offset, limit, order)


@router.get(
    "/v2/articles/{id}",
    responses={
        200: {"model": Article, "description": "OK"},
        400: {"description": "Bad Request, invalid Article ID format. "},
        404: {"description": "Article Not Found"},
    },
    tags=["v2/public"],
    summary="Get Article",
    response_model_by_alias=True,
)
async def get_article_by_id_v2(
    id: StrictStr = Path(..., description=""),
) -> Article:
    """Get an Article identified by it&#39;s unique ID"""
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2PublicApi.subclasses[0]().get_article_by_id_v2(id)


@router.get(
    "/v2/articles/versions/by-name/{name}",
    responses={
        200: {"model": ArticleVersion, "description": "OK"},
        400: {"description": "Bad Request, invalid Article name format. "},
        404: {"description": "Article Not Found"},
    },
    tags=["v2/public"],
    summary="Get ArticleVersion by name",
    response_model_by_alias=True,
)
async def get_article_by_name_v2(
    name: StrictStr = Path(..., description=""),
    wiki: Annotated[StrictStr, Field(description="The ID of the wiki of the Article")] = Query(None, description="The ID of the wiki of the Article", alias="wiki"),
    lan: Annotated[Optional[StrictStr], Field(description="Language of the ArticleVersion, if none, the original language will be returned")] = Query(None, description="Language of the ArticleVersion, if none, the original language will be returned", alias="lan"),
) -> ArticleVersion:
    """Get the most recent ArticleVersion the Article with the given name from the specified Wiki."""
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2PublicApi.subclasses[0]().get_article_by_name_v2(name, wiki, lan)


@router.get(
    "/v2/comments/articles/{article_id}",
    responses={
        200: {"model": CommentListResponse, "description": "OK"},
        400: {"description": "Bad Request, invalid parameters"},
        404: {"description": "Not Found"},
    },
    tags=["v2/public"],
    summary="Get Articles Comments",
    response_model_by_alias=True,
)
async def get_article_comments_v2(
    article_id: Annotated[StrictStr, Field(description="The unique ID of the article")] = Path(..., description="The unique ID of the article"),
    order: Annotated[Optional[StrictStr], Field(description="Set the order the comments will be shown. It is determined by date")] = Query('recent', description="Set the order the comments will be shown. It is determined by date", alias="order"),
    limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="Maximum amount of responses to be returned")] = Query(20, description="Maximum amount of responses to be returned", alias="limit", ge=0, le=100),
    offset: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")] = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset", ge=0),
    creation_date: Annotated[Optional[date], Field(description="Single date or range")] = Query(None, description="Single date or range", alias="creation_date"),
) -> CommentListResponse:
    """Retrieves all comments from an articles"""
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2PublicApi.subclasses[0]().get_article_comments_v2(article_id, order, limit, offset, creation_date)


@router.get(
    "/v2/wikis/{wiki_name}/articles/{article_name}",
    responses={
        200: {"model": ArticleVersion, "description": "OK"},
        400: {"description": "Bad Request"},
        404: {"description": "Not Found"},
    },
    tags=["v2/public"],
    summary="Get Article From Specific Wiki",
    response_model_by_alias=True,
)
async def get_article_from_specific_wiki_v2(
    wiki_name: Annotated[StrictStr, Field(description="Name of the wiki")] = Path(..., description="Name of the wiki"),
    article_name: Annotated[StrictStr, Field(description="Name of the article")] = Path(..., description="Name of the article"),
    lan: Annotated[Optional[StrictStr], Field(description="Language of the ArticleVersion, if none, the original language will be returned")] = Query(None, description="Language of the ArticleVersion, if none, the original language will be returned", alias="lan"),
) -> ArticleVersion:
    """Get the most recent ArticleVersion the Article with the given name from the Wiki with the given name. Endpoint thought to access articles when only the names of the Wiki and Article are known, with a textual URL for example."""
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2PublicApi.subclasses[0]().get_article_from_specific_wiki_v2(wiki_name, article_name, lan)


@router.get(
    "/v2/articles/versions/{id}/body",
    responses={
        200: {"model": ArticleVersionBody, "description": "OK. Parsed Succesfully."},
        404: {"description": "ArticleVersion Not Found"},
    },
    tags=["v2/public"],
    summary="Get ArticleVersion body",
    response_model_by_alias=True,
)
async def get_article_version_body_by_idv2(
    id: StrictStr = Path(..., description=""),
    parsed: Annotated[Optional[StrictBool], Field(description="It indicates if the body must be parsed.")] = Query(False, description="It indicates if the body must be parsed.", alias="parsed"),
    lan: Annotated[Optional[StrictStr], Field(description="Language of the body, if parsed, original language if not specified")] = Query(None, description="Language of the body, if parsed, original language if not specified", alias="lan"),
) -> ArticleVersionBody:
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2PublicApi.subclasses[0]().get_article_version_body_by_idv2(id, parsed, lan)


@router.get(
    "/v2/articles/versions/{id}",
    responses={
        200: {"model": ArticleVersion, "description": "OK"},
        400: {"description": "Bad Request, invalid ArticleVersion ID format. "},
        404: {"description": "Article Version Not Found"},
    },
    tags=["v2/public"],
    summary="Get ArticleVersion",
    response_model_by_alias=True,
)
async def get_article_version_by_id_v2(
    id: StrictStr = Path(..., description=""),
    lan: Annotated[Optional[StrictStr], Field(description="Language of the ArticleVersion, if none, the original language will be returned")] = Query(None, description="Language of the ArticleVersion, if none, the original language will be returned", alias="lan"),
) -> ArticleVersion:
    """Get an ArticleVersion identified by it&#39;s unique ID"""
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2PublicApi.subclasses[0]().get_article_version_by_id_v2(id, lan)


@router.get(
    "/v2/articles/{id}/versions",
    responses={
        200: {"model": ArticleVersionList, "description": "OK"},
        400: {"description": "Bad Request, invalid input paramaters"},
        404: {"description": "Article not Found"},
    },
    tags=["v2/public"],
    summary="Get Article&#39;s ArticleVersions",
    response_model_by_alias=True,
)
async def get_article_version_list_by_article_idv2(
    id: StrictStr = Path(..., description=""),
    offset: Annotated[Optional[StrictInt], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")] = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset"),
    limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="The maximum number of results to return.")] = Query(20, description="The maximum number of results to return.", alias="limit", ge=0, le=100),
    order: Annotated[Optional[StrictStr], Field(description="Sorts the articles by different criteria")] = Query(None, description="Sorts the articles by different criteria", alias="order"),
) -> ArticleVersionList:
    """Get a list of ArticleVersions of a given Article. Results can be sorted by creation date adn support pagination."""
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2PublicApi.subclasses[0]().get_article_version_list_by_article_idv2(id, offset, limit, order)


@router.get(
    "/v2/articles/commented_by/{id}",
    responses={
        200: {"model": ArticleList, "description": "OK"},
        400: {"description": "Bad Request, inavalid User ID format"},
        404: {"description": "User Not Found"},
    },
    tags=["v2/public"],
    summary="Get Articles commented by User",
    response_model_by_alias=True,
)
async def get_articles_commented_by_user_v2(
    id: StrictStr = Path(..., description=""),
    offset: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")] = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset", ge=0),
    limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="The maximum number of results to return.")] = Query(20, description="The maximum number of results to return.", alias="limit", ge=0, le=100),
    order: Annotated[Optional[StrictStr], Field(description="Sorts the articles by different criteria")] = Query(None, description="Sorts the articles by different criteria", alias="order"),
) -> ArticleList:
    """Get a list of the Articles commented by a given user."""
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2PublicApi.subclasses[0]().get_articles_commented_by_user_v2(id, offset, limit, order)


@router.get(
    "/v2/tags/articles/{id}",
    responses={
        200: {"model": TagList, "description": "OK"},
        404: {"description": "Article not found"},
    },
    tags=["v2/public"],
    summary="Get Articles Tag",
    response_model_by_alias=True,
)
async def get_articles_tags_v2(
    id: StrictStr = Path(..., description=""),
    limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="Maximum amount of responses to be returned")] = Query(20, description="Maximum amount of responses to be returned", alias="limit", ge=0, le=100),
    offset: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")] = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset", ge=0),
) -> TagList:
    """Retrieves all the tags from an article."""
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2PublicApi.subclasses[0]().get_articles_tags_v2(id, limit, offset)


@router.get(
    "/v2/ratings/{id}",
    responses={
        200: {"model": Rating, "description": "Rating found and returned"},
        400: {"description": "Bad Request, invalid Rating ID format"},
        404: {"description": "Rating Not Found"},
    },
    tags=["v2/public"],
    summary="Get Rating",
    response_model_by_alias=True,
)
async def get_rating_v2(
    id: StrictStr = Path(..., description=""),
) -> Rating:
    """Get the Rating with the provided ID"""
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2PublicApi.subclasses[0]().get_rating_v2(id)


@router.get(
    "/v2/ratings/articles/{articleId}/users/{userId}",
    responses={
        200: {"model": Rating, "description": "OK"},
        404: {"description": "Not Found"},
        422: {"description": "Unprocessable Entity (WebDAV)"},
    },
    tags=["v2/public"],
    summary="Get rating made by an user in an article",
    response_model_by_alias=True,
)
async def get_ratings_bu_user_on_article_v2(
    articleId: StrictStr = Path(..., description=""),
    userId: StrictStr = Path(..., description=""),
) -> Rating:
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2PublicApi.subclasses[0]().get_ratings_bu_user_on_article_v2(articleId, userId)


@router.get(
    "/v2/tags/{id}",
    responses={
        200: {"model": Tag, "description": "OK"},
        400: {"description": "Bad Request, invalid Tag ID format"},
        403: {"description": "Forbidden"},
        404: {"description": "Tag not found"},
    },
    tags=["v2/public"],
    summary="Get Tag",
    response_model_by_alias=True,
)
async def get_tag_v2(
    id: StrictStr = Path(..., description=""),
) -> Tag:
    """Get a tag by ID. """
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2PublicApi.subclasses[0]().get_tag_v2(id)


@router.get(
    "/v2/comments/users/{user_id}",
    responses={
        200: {"model": CommentListResponse, "description": "OK"},
        400: {"description": "Bad Request, invalid User ID format"},
        404: {"description": "Not Found"},
    },
    tags=["v2/public"],
    summary="Get Users Comments",
    response_model_by_alias=True,
)
async def get_users_comments_v2(
    user_id: Annotated[StrictStr, Field(description="The unique ID of the user")] = Path(..., description="The unique ID of the user"),
    article_id: Annotated[Optional[StrictStr], Field(description="Fillters the results by the article's ID")] = Query(None, description="Fillters the results by the article&#39;s ID", alias="article_id"),
    order: Annotated[Optional[StrictStr], Field(description="Set the order the comments will be shown. It is determined by date")] = Query('recent', description="Set the order the comments will be shown. It is determined by date", alias="order"),
    limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="Maximum amount of responses to be returned")] = Query(20, description="Maximum amount of responses to be returned", alias="limit", ge=0, le=100),
    offset: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")] = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset", ge=0),
    creation_date: Annotated[Optional[date], Field(description="Single date or range")] = Query(None, description="Single date or range", alias="creation_date"),
) -> CommentListResponse:
    """Retrieves all comments from an user"""
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2PublicApi.subclasses[0]().get_users_comments_v2(user_id, article_id, order, limit, offset, creation_date)


@router.get(
    "/v2/tags/wikis/{id}",
    responses={
        200: {"model": TagList, "description": "OK"},
        400: {"description": "Bad Request, invalid parameters"},
        404: {"description": "Wiki not found"},
    },
    tags=["v2/public"],
    summary="Get Wikis Tags",
    response_model_by_alias=True,
)
async def get_wiki_tags_v2(
    id: Annotated[StrictStr, Field(description="The unique ID of the wiki.")] = Path(..., description="The unique ID of the wiki."),
    limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="Maximum amount of responses to be returned")] = Query(20, description="Maximum amount of responses to be returned", alias="limit", ge=0, le=100),
    offset: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")] = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset", ge=0),
) -> TagList:
    """Retrieve all the tags from a wiki."""
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2PublicApi.subclasses[0]().get_wiki_tags_v2(id, limit, offset)


@router.get(
    "/v2/wikis/{id_name}",
    responses={
        200: {"model": Wiki, "description": "Succesful operation."},
        400: {"description": "Bad Request"},
        404: {"description": "Bad Request. Wiki not found."},
    },
    tags=["v2/public"],
    summary="Get Wiki",
    response_model_by_alias=True,
)
async def get_wiki_v2(
    id_name: Annotated[StrictStr, Field(description="Identifier of the requested wiki, may be its name or its ID. Keep in mind wiki names may be modified.")] = Path(..., description="Identifier of the requested wiki, may be its name or its ID. Keep in mind wiki names may be modified."),
    lang: Annotated[Optional[StrictStr], Field(description="Language of the wiki to retrieve.")] = Query(None, description="Language of the wiki to retrieve.", alias="lang"),
    token_oauth_token: TokenModel = Security(
        get_token_oauth_token
    ),
) -> Wiki:
    """Get Wiki with the matching ID."""
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2PublicApi.subclasses[0]().get_wiki_v2(id_name, lang)


@router.post(
    "/v2/comments/articles/{article_id}",
    responses={
        201: {"model": Comment, "description": "Comment successufully created"},
        400: {"description": "Bad Request, wrong content structure"},
        403: {"description": "Forbidden"},
        404: {"description": "Article or Author not found"},
    },
    tags=["v2/public"],
    summary="Post Comment",
    response_model_by_alias=True,
)
async def post_comment_v2(
    article_id: Annotated[StrictStr, Field(description="The unique ID of the article")] = Path(..., description="The unique ID of the article"),
    new_comment: Annotated[Optional[NewComment], Field(description="JSON object that contains the author and content of the comment")] = Body(None, description="JSON object that contains the author and content of the comment"),
    token_oauth_token: TokenModel = Security(
        get_token_oauth_token
    ),
) -> Comment:
    """Posts a new comment in an article"""
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2PublicApi.subclasses[0]().post_comment_v2(article_id, new_comment)


@router.post(
    "/v2/ratings/articles/{id}",
    responses={
        201: {"model": Rating, "description": "Rating created"},
        400: {"description": "Bad Request, invalid Article ID format"},
        403: {"description": "Forbidden"},
        404: {"description": "Not Found"},
    },
    tags=["v2/public"],
    summary="Rate Article",
    response_model_by_alias=True,
)
async def rate_article_v2(
    id: StrictStr = Path(..., description=""),
    new_rating: Optional[NewRating] = Body(None, description=""),
    token_oauth_token: TokenModel = Security(
        get_token_oauth_token
    ),
) -> Rating:
    """Create a rating for a given Article"""
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2PublicApi.subclasses[0]().rate_article_v2(id, new_rating)


@router.get(
    "/v2/articles",
    responses={
        200: {"model": ArticleList, "description": "OK"},
        400: {"description": "Bad Request, invalid input paramaters"},
        404: {"description": "Article Not Found"},
    },
    tags=["v2/public"],
    summary="Search for Articles",
    response_model_by_alias=True,
)
async def search_articles_v2(
    wiki_id: Annotated[Optional[StrictStr], Field(description="The ID of the wiki where the serch will be made")] = Query(None, description="The ID of the wiki where the serch will be made", alias="wiki_id"),
    name: Annotated[Optional[StrictStr], Field(description="Search query for the name of the article")] = Query(None, description="Search query for the name of the article", alias="name"),
    tags: Annotated[Optional[List[StrictStr]], Field(description="A comma-separated list of tag IDs to search for")] = Query(None, description="A comma-separated list of tag IDs to search for", alias="tags"),
    offset: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")] = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset", ge=0),
    limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="The maximum number of results to return.")] = Query(20, description="The maximum number of results to return.", alias="limit", ge=0, le=100),
    order: Annotated[Optional[StrictStr], Field(description="Sorts the articles by different criteria")] = Query('none', description="Sorts the articles by different criteria", alias="order"),
    creation_date: Annotated[Optional[date], Field(description="Single date or range")] = Query(None, description="Single date or range", alias="creation_date"),
    author_name: Annotated[Optional[StrictStr], Field(description="Filter for the author of the Article")] = Query(None, description="Filter for the author of the Article", alias="author_name"),
    editor_name: Annotated[Optional[StrictStr], Field(description="Filter for the editors of the Article")] = Query(None, description="Filter for the editors of the Article", alias="editor_name"),
    lan: Annotated[Optional[StrictStr], Field(description="Language of the ArticleVersion, if none, the original language will be returned")] = Query(None, description="Language of the ArticleVersion, if none, the original language will be returned", alias="lan"),
) -> ArticleList:
    """Get a list of Articles from a given Wiki that match a keyword string. Results can by filtered by tags, sorted by different parameters and support pagination."""
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2PublicApi.subclasses[0]().search_articles_v2(wiki_id, name, tags, offset, limit, order, creation_date, author_name, editor_name, lan)


@router.get(
    "/v2/wikis",
    responses={
        200: {"model": WikiList, "description": "Succesful operation."},
        400: {"description": "Bad Request, invalid parameters"},
        418: {"description": "The server refused to brew coffee. &lt;br/&gt; *Yes, this is a joke. Yes, this is a reserved HTTP response code since 1998.* &lt;br/&gt; *See [RFC 2324](https://datatracker.ietf.org/doc/html/rfc2324) for more information. Actually, do not.*"},
    },
    tags=["v2/public"],
    summary="Search for Wikis",
    response_model_by_alias=True,
)
async def search_wikis_v2(
    name: Annotated[Optional[StrictStr], Field(description="String to be searched within the wiki's name.")] = Query(None, description="String to be searched within the wiki&#39;s name.", alias="name"),
    limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=1)]], Field(description="Maximum amount of results to be returned.")] = Query(20, description="Maximum amount of results to be returned.", alias="limit", ge=1, le=100),
    offset: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")] = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset", ge=0),
    order: Annotated[Optional[date], Field(description="Sorts the wikis by different criteria")] = Query(None, description="Sorts the wikis by different criteria", alias="order"),
    creation_date: Annotated[Optional[StrictStr], Field(description="Single date or range")] = Query(None, description="Single date or range", alias="creation_date"),
    author_name: Annotated[Optional[StrictStr], Field(description="Filter for the author of the Wiki")] = Query(None, description="Filter for the author of the Wiki", alias="author_name"),
    lang: Annotated[Optional[StrictStr], Field(description="Language of the wiki to retrieve.")] = Query(None, description="Language of the wiki to retrieve.", alias="lang"),
) -> WikiList:
    """Get a list of Wikis that match a keyword string. Results can by filtered by tags, sorted by different parameters and support pagination."""
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2PublicApi.subclasses[0]().search_wikis_v2(name, limit, offset, order, creation_date, author_name, lang)