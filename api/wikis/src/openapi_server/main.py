# coding: utf-8

"""
    Wiki API

    This API is used to perform operations on the wikis of laWiki

    The version of the OpenAPI document: 1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from fastapi import FastAPI

from openapi_server.apis.default_api import router as DefaultApiRouter

app = FastAPI(
    title="Wiki API",
    description="This API is used to perform operations on the wikis of laWiki",
    version="1.0",
)

app.include_router(DefaultApiRouter)