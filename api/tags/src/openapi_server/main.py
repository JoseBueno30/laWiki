# coding: utf-8

"""
    TagAPI

    API for the tags microservice of laWiki web appplication. It provides all endpoints related to CRUD operatios for wiki tags.

    The version of the OpenAPI document: 1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from fastapi import FastAPI

from openapi_server.apis.admins_api import router as AdminsApiRouter
from openapi_server.apis.default_api import router as DefaultApiRouter
from openapi_server.apis.editors_api import router as EditorsApiRouter

app = FastAPI(
    title="TagAPI",
    description="API for the tags microservice of laWiki web appplication. It provides all endpoints related to CRUD operatios for wiki tags.",
    version="1.0",
)

app.include_router(AdminsApiRouter)
app.include_router(DefaultApiRouter)
app.include_router(EditorsApiRouter)
