# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil


from openapi_server.apis.v2_apis.v2_editors_api_base import BaseV2EditorsApi
import openapi_server.impl.v2_impl

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
    status, File, UploadFile
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from openapi_server.models.article import Article
from openapi_server.models.article_version import ArticleVersion
from openapi_server.models.inline_response200 import InlineResponse200
from openapi_server.models.new_article import NewArticle
from openapi_server.models.new_article_version import NewArticleVersion
from openapi_server.models.tag_id_list import TagIDList
from openapi_server.security_api import verify_token


router = APIRouter()

ns_pkg = openapi_server.impl.v2_impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.put(
    "/v2/tags/articles/{id}",
    responses={
        204: {"description": "No Content, tags assigned"},
        400: {"description": "Bad Request, invalid paramaters format"},
        403: {"description": "Forbidden"},
        404: {"description": "Article or tag not found"},
    },
    tags=["v2/editors"],
    summary="Assign Tags",
    response_model_by_alias=True,
)
async def assign_tags(
    id: str = Path(..., description=""),
    tag_id_list: TagIDList = Body(None, description=""),
    decoded_token: TokenModel = Security(
        verify_token
    ),
) -> None:
    """Assigns a list of tags, given their IDs, to an article."""
    if not BaseV2EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2EditorsApi.subclasses[0]().assign_tags(id, tag_id_list, decoded_token)


@router.post(
    "/v2/articles",
    responses={
        201: {"model": Article, "description": "Created"},
        400: {"description": "Bad Request, invalid paramaters"},
        403: {"description": "Forbidden"},
    },
    tags=["v2/editors"],
    summary="Create Article",
    response_model_by_alias=True,
)
async def create_article(
    new_article: NewArticle = Body(None, description=""),
    decoded_token: TokenModel = Security(
        verify_token
    ),
) -> Article:
    """Create a new Article in a given wiki"""
    if not BaseV2EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2EditorsApi.subclasses[0]().create_article(new_article, decoded_token)


@router.post(
    "/v2/articles/{id}/versions",
    responses={
        201: {"model": ArticleVersion, "description": "Version successfully created."},
        400: {"description": "Bad Request, Invalid Parameters"},
        403: {"description": "Forbidden"},
    },
    tags=["v2/editors"],
    summary="Create ArticleVersion for an Article",
    response_model_by_alias=True,
)
async def create_article_version(
    id: str = Path(..., description=""),
    new_article_version: NewArticleVersion = Body(None, description=""),
    decoded_token: TokenModel = Security(
        verify_token
    ),
) -> ArticleVersion:
    """Create an ArticleVersion for a given Article and adds it to the list of versions of the Article."""
    if not BaseV2EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2EditorsApi.subclasses[0]().create_article_version(id, new_article_version, decoded_token)


@router.delete(
    "/v2/articles/{id}",
    responses={
        200: {"description": "Article successfully deleted."},
        400: {"description": "Bad Request, invalid Article ID format. "},
        403: {"description": "Forbidden"},
        404: {"description": "Article Not Found"},
    },
    tags=["v2/editors"],
    summary="Delete Article",
    response_model_by_alias=True,
)
async def delete_article_by_id(
    id: str = Path(..., description=""),
    decoded_token: TokenModel = Security(
        verify_token
    ),
) -> None:
    """Delete an Article identified by it&#39;s unique ID"""
    if not BaseV2EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2EditorsApi.subclasses[0]().delete_article_by_id(id, decoded_token)


@router.delete(
    "/v2/articles/versions/{id}",
    responses={
        200: {"description": "ArticleVersion successfully deleted."},
        400: {"description": "Bad Request, invalid ArticleVersion ID format. "},
        403: {"description": "Forbidden"},
        404: {"description": "ArticleVersion Not Found"},
    },
    tags=["v2/editors"],
    summary="Delete ArticleVersion",
    response_model_by_alias=True,
)
async def delete_article_version_by_id(
    id: str = Path(..., description=""),
    decoded_token: TokenModel = Security(
        verify_token
    ),
) -> None:
    """Delete an ArticleVersion identified by it&#39;s unique ID"""
    if not BaseV2EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2EditorsApi.subclasses[0]().delete_article_version_by_id(id, decoded_token)


@router.put(
    "/v2/articles/{article_id}/versions/{version_id}",
    responses={
        200: {"description": "ArticleVersion successfully restored"},
        400: {"description": "invalid Article or ArticleVersion ID format"},
        403: {"description": "Forbidden"},
        404: {"description": "Article Version Not Found"},
    },
    tags=["v2/editors"],
    summary="Restore ArticleVersion",
    response_model_by_alias=True,
)
async def restore_article_version(
    article_id: str = Path(..., description=""),
    version_id: str = Path(..., description=""),
    decoded_token: TokenModel = Security(
        verify_token
    ),
) -> None:
    """Restore an older ArticleVersion of an Article."""
    if not BaseV2EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2EditorsApi.subclasses[0]().restore_article_version(article_id, version_id, decoded_token)


@router.delete(
    "/v2/tags/articles/{id}",
    responses={
        204: {"description": "No Content, tag unassigned succesfully"},
        400: {"description": "Bad Request, invalid invalid paramaters format"},
        403: {"description": "Forbidden"},
        404: {"description": "Article or tag not found"},
    },
    tags=["v2/editors"],
    summary="Unassign Tags",
    response_model_by_alias=True,
)
async def unassign_tags(
    id: str = Path(..., description=""),
    ids: List[str] = Query(None, description="List of Tag IDs", alias="ids"),
    decoded_token: TokenModel = Security(
        verify_token
    ),
) -> None:
    """Unassigns a list of tags, given their IDs to an article."""
    if not BaseV2EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2EditorsApi.subclasses[0]().unassign_tags(id, ids, decoded_token)


@router.post(
    "/v2/upload-image",
    responses={
        200: {"model": InlineResponse200, "description": "Successfully uploaded"},
        400: {"description": "Bad Request"},
        401: {"description": "Unauthorized"},
    },
    tags=["v2/editors"],
    summary="Upload Image",
    response_model_by_alias=True
)
async def upload_image(
    file: UploadFile = File(..., description="Image to upload"),
    decoded_token: TokenModel = Security(
        verify_token
    ),
) -> InlineResponse200:
    """Uploads an image file and returns the URL."""
    if not BaseV2EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2EditorsApi.subclasses[0]().upload_image(file)
