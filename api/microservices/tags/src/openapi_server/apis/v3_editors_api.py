# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from bson.errors import InvalidId

from openapi_server.apis.v3_editors_api_base import BaseV3EditorsApi
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
    "/v3/tags/articles/{id}",
    responses={
        204: {"description": "No Content, tags assigned"},
        400: {"description": "Bad Request, invalid parameters format"},
        403: {"description": "Forbidden"},
        404: {"description": "Article or tag not found"},
    },
    tags=["v3/editors"],
    summary="Assign Tags",
    response_model_by_alias=True,
)
async def assign_tags_v3(
    id: str = Path(..., description=""),
    user_id: str = Header(None, description=""),
    admin: bool = Header(None, description=""),
    tag_id_list: TagIDList = Body(None, description=""),
) -> None:
    """Assigns a list of tags, given their IDs, to an article."""
    if not BaseV3EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseV3EditorsApi.subclasses[0]().assign_tags_v3(id, user_id, admin, tag_id_list)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Bad request, invalid Article ID format")
    except KeyError:
        raise HTTPException(status_code=404, detail="Article not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/v3/tags/{id}",
    responses={
        204: {"description": "No Content, tag deleted successfully"},
        400: {"description": "Bad Request, invalid ID format"},
        403: {"description": "Forbidden"},
        404: {"description": "Tag not found"},
    },
    tags=["v3/editors"],
    summary="Delete Tag",
    response_model_by_alias=True,
)
async def delete_tag_v3(
    id: str = Path(..., description=""),
    user_id: str = Header(None, description=""),
    admin: bool = Header(None, description=""),
) -> None:
    """Delete a wiki tag."""
    if not BaseV3EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseV3EditorsApi.subclasses[0]().delete_tag_v3(id, user_id, admin)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Bad request, invalid Tag ID format")
    except KeyError:
        raise HTTPException(status_code=404, detail="Tag not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/v3/tags/wikis/{id}",
    responses={
        200: {"model": TagV2, "description": "OK"},
        400: {"description": "Bad Request, wrong content structure"},
        403: {"description": "Forbidden"},
    },
    tags=["v3/editors"],
    summary="Create Tag",
    response_model_by_alias=True,
)
async def post_wiki_tag_v3(
    id: str = Path(..., description="The unique ID of the wiki."),
    user_id: str = Header(None, description=""),
    admin: bool = Header(None, description=""),
    new_tag_v2: NewTagV2 = Body(None, description=""),
) -> TagV2:
    """Create a new tag in a given wiki."""
    if not BaseV3EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseV3EditorsApi.subclasses[0]().post_wiki_tag_v3(id, user_id, admin, new_tag_v2)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Bad request, invalid Wiki ID format")
    except KeyError:
        raise HTTPException(status_code=404, detail="Wiki not found")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/v3/tags/articles/{id}",
    responses={
        204: {"description": "No Content, tags unassigned successfully"},
        400: {"description": "Bad Request, invalid parameters format"},
        403: {"description": "Forbidden"},
        404: {"description": "Article or tag not found"},
    },
    tags=["v3/editors"],
    summary="Unassign Tags",
    response_model_by_alias=True,
)
async def unassign_tags_v3(
    id: str = Path(..., description=""),
    ids: List[str] = Query(None, description="List of Tag IDs", alias="ids"),
    user_id: str = Header(None, description=""),
    admin: bool = Header(None, description=""),
) -> None:
    """Unassigns a list of tags, given their IDs to an article."""
    if not BaseV3EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseV3EditorsApi.subclasses[0]().unassign_tags_v3(id, ids, user_id, admin)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Bad request, invalid Article ID format")
    except KeyError:
        raise HTTPException(status_code=404, detail="Article not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
