# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from bson.errors import InvalidId

from openapi_server.apis.v2_editors_api_base import BaseV2EditorsApi
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
from openapi_server.models.new_tag_v2 import NewTagV2
from openapi_server.models.tag_id_list import TagIDList
from openapi_server.models.tag_v2 import TagV2


router = APIRouter()

ns_pkg = openapi_server.impl
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
async def assign_tags_v2(
    id: str = Path(..., description=""),
    tag_id_list: TagIDList = Body(None, description=""),
) -> None:
    """Assigns a list of tags, given their IDs, to an article."""
    if not BaseV2EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseV2EditorsApi.subclasses[0]().assign_tags_v2(id, tag_id_list)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Bad request, invalid Article ID format")
    except KeyError:
        raise HTTPException(status_code=404, detail="Article not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/v2/tags/{id}",
    responses={
        204: {"description": "No Content, tag deleted succesfully"},
        400: {"description": "Bad Request, invalid ID format"},
        403: {"description": "Forbidden"},
        404: {"description": "Tag not found"},
    },
    tags=["v2/editors"],
    summary="Delete Tag",
    response_model_by_alias=True,
)
async def delete_tag_v2(
    id: str = Path(..., description=""),
) -> None:
    """Delete a wiki tag."""
    if not BaseV2EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseV2EditorsApi.subclasses[0]().delete_tag_v2(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Bad request, invalid Tag ID format")
    except KeyError:
        raise HTTPException(status_code=404, detail="Tag not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/v2/tags/wikis/{id}",
    responses={
        200: {"model": TagV2, "description": "OK"},
        400: {"description": "Bad Request, wrong content structure"},
        403: {"description": "Forbidden"},
    },
    tags=["v2/editors"],
    summary="Create Tag",
    response_model_by_alias=True,
)
async def post_wiki_tag_v2(
    id: str = Path(..., description="The unique ID of the wiki."),
    new_tag_v2: NewTagV2 = Body(None, description=""),
) -> TagV2:
    """Create a new tag in a given wiki."""
    if not BaseV2EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseV2EditorsApi.subclasses[0]().post_wiki_tag_v2(id, new_tag_v2)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Bad request, invalid Wiki ID format")
    except KeyError:
        raise HTTPException(status_code=404, detail="Wiki not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
async def unassign_tags_v2(
    id: str = Path(..., description=""),
    ids: list[str] = Query(None, description="List of Tag IDs", alias="ids"),
) -> None:
    """Unassigns a list of tags, given their IDs to an article."""
    if not BaseV2EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseV2EditorsApi.subclasses[0]().unassign_tags_v2(id, ids)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Bad request, invalid Article ID format")
    except KeyError:
        raise HTTPException(status_code=404, detail="Article not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
