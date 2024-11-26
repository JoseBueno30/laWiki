# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from bson.errors import InvalidId

from openapi_server.apis.v1_editors_api_base import BaseV1EditorsApi
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
from openapi_server.models.new_tag import NewTag
from openapi_server.models.tag import Tag
from openapi_server.models.tag_id_list import TagIDList


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.put(
    "/v1/tags/articles/{id}",
    responses={
        204: {"description": "No Content, tags assigned"},
        400: {"description": "Bad Request, invalid paramaters format"},
        403: {"description": "Forbidden"},
        404: {"description": "Article or tag not found"},
    },
    tags=["v1/editors"],
    summary="Assign Tags",
    response_model_by_alias=True,
)
async def assign_tags_v1(
    id: str = Path(..., description=""),
    tag_id_list: TagIDList = Body(None, description=""),
) -> None:
    """Assigns a list of tags, given their IDs, to an article."""
    if not BaseV1EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseV1EditorsApi.subclasses[0]().assign_tags_v1(id, tag_id_list)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Bad request, invalid parameters format")
    except KeyError:
        raise HTTPException(status_code=404, detail="Article not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/v1/tags/{id}",
    responses={
        204: {"description": "No Content, tag deleted succesfully"},
        400: {"description": "Bad Request, invalid ID format"},
        403: {"description": "Forbidden"},
        404: {"description": "Tag not found"},
    },
    tags=["v1/editors"],
    summary="Delete Tag",
    response_model_by_alias=True,
)
async def delete_tag_v1(
    id: str = Path(..., description=""),
) -> None:
    """Delete a wiki tag."""
    if not BaseV1EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseV1EditorsApi.subclasses[0]().delete_tag_v1(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Bad request, invalid Tag ID format")
    except KeyError:
        raise HTTPException(status_code=404, detail="Tag not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/v1/tags/wikis/{id}",
    responses={
        200: {"model": Tag, "description": "OK"},
        400: {"description": "Bad Request, wrong content structure"},
        403: {"description": "Forbidden"},
    },
    tags=["v1/editors"],
    summary="Create Tag",
    response_model_by_alias=True,
)
async def post_wiki_tag_v1(
    id: str = Path(..., description="The unique ID of the wiki."),
    new_tag: NewTag = Body(None, description=""),
) -> Tag:
    """Create a new tag in a given wiki."""
    if not BaseV1EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseV1EditorsApi.subclasses[0]().post_wiki_tag_v1(id, new_tag)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Bad request, wrong content structure")
    except KeyError:
        raise HTTPException(status_code=404, detail="Wiki not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/v1/tags/articles/{id}",
    responses={
        204: {"description": "No Content, tag unassigned succesfully"},
        400: {"description": "Bad Request, invalid invalid paramaters format"},
        403: {"description": "Forbidden"},
        404: {"description": "Article or tag not found"},
    },
    tags=["v1/editors"],
    summary="Unassign Tags",
    response_model_by_alias=True,
)
async def unassign_tags_v1(
    id: str = Path(..., description=""),
    ids: List[str] = Query(None, description="List of Tag IDs", alias="ids"),
) -> None:
    """Unassigns a list of tags, given their IDs to an article."""
    if not BaseV1EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseV1EditorsApi.subclasses[0]().unassign_tags_v1(id, ids)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Bad request, invalid ID format")
    except KeyError:
        raise HTTPException(status_code=404, detail="Article not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
