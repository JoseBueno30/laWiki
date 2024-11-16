# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.admins_v2_api_base import BaseAdminsV2Api
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
from openapi_server.models.new_wiki_v2 import NewWikiV2
from openapi_server.models.wiki_v2 import WikiV2


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.delete(
    "/v2/wikis/{id_name}",
    responses={
        200: {"description": "Removed successfully. Returned deleted item."},
        400: {"description": "Bad Request."},
        403: {"description": "Forbidden. User is not authorized to delete wikis."},
        404: {"description": "Wiki not found."},
    },
    tags=["adminsV2"],
    summary="Remove Wiki",
    response_model_by_alias=True,
)
async def remove_wiki_v2(
    id_name: str = Path(..., description="Identifier of the requested wiki, may be its name or its ID. Keep in mind wiki names may be modified."),
) -> None:
    """Remove Wiki with the matching ID."""
    if not BaseAdminsV2Api.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAdminsV2Api.subclasses[0]().remove_wiki_v2(id_name)


@router.put(
    "/v2/wikis/{id_name}",
    responses={
        200: {"model": WikiV2, "description": "Succesful operation."},
        400: {"description": "Bad Request"},
        403: {"description": "Forbidden. User is not authorized to edit wiki the requested wiki."},
        404: {"description": "Bad Request. Wiki not found."},
    },
    tags=["adminsV2"],
    summary="Update Wiki",
    response_model_by_alias=True,
)
async def update_wiki_v2(
    id_name: str = Path(..., description="Identifier of the requested wiki, may be its name or its ID. Keep in mind wiki names may be modified."),
    new_wiki_v2: NewWikiV2 = Body(None, description=""),
) -> WikiV2:
    """Update Wiki with wiki the matching ID"""
    if not BaseAdminsV2Api.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAdminsV2Api.subclasses[0]().update_wiki_v2(id_name, new_wiki_v2)