# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from bson.errors import InvalidId

from openapi_server.apis.admins_api_base import BaseAdminsApi
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


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.delete(
    "/tags/{id}",
    responses={
        204: {"description": "No Content, tag deleted succesfully"},
        400: {"description": "Bad Request, invalid ID format"},
        403: {"description": "Forbidden"},
        404: {"description": "Tag not found"},
    },
    tags=["admins"],
    summary="Delete Tag",
    response_model_by_alias=True,
)
async def delete_tag(
    id: str = Path(..., description=""),
) -> None:
    """Delete a wiki tag."""
    if not BaseAdminsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseAdminsApi.subclasses[0]().delete_tag(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Bad request, invalid Tag ID format")
    except KeyError:
        raise HTTPException(status_code=404, detail="Tag not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/tags/wikis/{id}",
    responses={
        200: {"model": Tag, "description": "OK"},
        400: {"description": "Bad Request, wrong content structure"},
        403: {"description": "Forbidden"},
    },
    tags=["admins"],
    summary="Create Tag",
    response_model_by_alias=True,
)
async def post_wiki_tag(
    id: str = Path(..., description="The unique ID of the wiki."),
    new_tag: NewTag = Body(None, description=""),
) -> Tag:
    """Create a new tag in a given wiki."""
    if not BaseAdminsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseAdminsApi.subclasses[0]().post_wiki_tag(id, new_tag)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Bad request, invalid Wiki ID format")
    except KeyError:
        raise HTTPException(status_code=404, detail="Wiki not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
