# coding: utf-8

"""
    Wiki API

    This API is used to perform operations on the wikis of laWiki

    The version of the OpenAPI document: 1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from fastapi import FastAPI

from openapi_server.apis.admins_api import router as AdminsApiRouter
from openapi_server.apis.default_api import router as DefaultApiRouter
from openapi_server.apis.internal_api import router as InternalApiRouter
from openapi_server.apis.admins_api_v2 import router as AdminsApiRouterV2
from openapi_server.apis.default_api_v2 import router as DefaultApiRouterV2
from openapi_server.apis.internal_api_v2 import router as InternalApiRouterV2

app = FastAPI(
    title="Wiki API",
    description="This API is used to perform operations on the wikis of laWiki",
    version="1.0",
)

app.include_router(AdminsApiRouter)
app.include_router(DefaultApiRouter)
app.include_router(InternalApiRouter)
app.include_router(AdminsApiRouterV2)
app.include_router(DefaultApiRouterV2)
app.include_router(InternalApiRouterV2)
