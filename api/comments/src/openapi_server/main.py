# coding: utf-8

"""
    CommentsAPI

    API for the Comments microservice of laWiki web appplication. It provides all endpoints related to CRUD operatios for articles comments.

    The version of the OpenAPI document: 0.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from fastapi import FastAPI

from openapi_server.apis.default_api import router as DefaultApiRouter

app = FastAPI(
    title="CommentsAPI",
    description="API for the Comments microservice of laWiki web appplication. It provides all endpoints related to CRUD operatios for articles comments.",
    version="0.1",
)

app.include_router(DefaultApiRouter)
