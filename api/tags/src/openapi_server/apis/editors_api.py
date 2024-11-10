# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from bson.errors import InvalidId

from openapi_server.apis.editors_api_base import BaseEditorsApi
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
from openapi_server.models.tag_id_list import TagIDList


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.put(
    "/tags/articles/{id}",
    responses={
        204: {"description": "No Content, tags assigned successfully"},
        400: {"description": "Bad Request, invalid paramaters format"},
        403: {"description": "Forbidden"},
        404: {"description": "Article or tag not found"},
    },
    tags=["editors"],
    summary="Assign Tags",
    response_model_by_alias=True,
)
async def assign_tags(
    id: str = Path(..., description=""),
    tag_id_list: TagIDList = Body(None, description=""),
) -> None:
    """Assigns a list of tags, given their IDs, to an article."""
    if not BaseEditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseEditorsApi.subclasses[0]().assign_tags(id, tag_id_list)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Bad request, invalid ID format")
    except KeyError:
        raise HTTPException(status_code=404, detail="Article not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/tags/articles/{id}",
    responses={
        204: {"description": "No Content, tags unassigned successfully"},
        400: {"description": "Bad Request, invalid invalid paramaters format"},
        403: {"description": "Forbidden"},
        404: {"description": "Article or tag not found"},
    },
    tags=["editors"],
    summary="Unassign Tags",
    response_model_by_alias=True,
)
async def unassign_tags(
    id: str = Path(..., description=""),
    ids: list[str] = Query(None, description="List of Tag IDs", alias="ids"),
) -> None:
    """Unassigns a list of tags, given their IDs to an article."""
    if not BaseEditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseEditorsApi.subclasses[0]().unassign_tags(id, ids)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Bad request, invalid ID format")
    except KeyError:
        raise HTTPException(status_code=404, detail="Article not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
