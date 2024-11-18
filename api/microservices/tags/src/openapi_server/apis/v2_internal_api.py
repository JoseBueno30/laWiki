# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from bson.errors import InvalidId

from openapi_server.apis.v2_internal_api_base import BaseV2InternalApi
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


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.delete(
    "/v2/tags/wikis/{id}",
    responses={
        204: {"description": "No Content, tags deleted successfully"},
        400: {"description": "Bad Request, Incorrect ID format"},
        403: {"description": "Forbidden"},
        404: {"description": "Wiki not found"},
    },
    tags=["v2/internal"],
    summary="Delete Wiki Tags",
    response_model_by_alias=True,
)
async def delete_wiki_tags_v2(
    id: str = Path(..., description=""),
) -> None:
    """Delete all tags from a wiki."""
    if not BaseV2InternalApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseV2InternalApi.subclasses[0]().delete_wiki_tags_v2(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Bad request, invalid Wiki ID format")
    except KeyError:
        raise HTTPException(status_code=404, detail="Wiki not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
