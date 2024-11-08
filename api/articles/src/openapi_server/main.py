# coding: utf-8

"""
    ArticlesAPI

    The Articles API provides endpoints for managing and retrieving articles and article versions within the wiki application. It supports core CRUD (Create, Read, Update, Delete) operations, search functionality, and versioning.

    The version of the OpenAPI document: 1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from fastapi import FastAPI

from openapi_server.apis.default_api import router as DefaultApiRouter
from openapi_server.apis.editors_api import router as EditorsApiRouter

app = FastAPI(
    title="ArticlesAPI",
    description="The Articles API provides endpoints for managing and retrieving articles and article versions within the wiki application. It supports core CRUD (Create, Read, Update, Delete) operations, search functionality, and versioning.",
    version="1.0",
)

app.include_router(DefaultApiRouter)
app.include_router(EditorsApiRouter)