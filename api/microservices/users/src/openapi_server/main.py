# coding: utf-8

"""
    UsersAPI

    Microservice that manages authentication and user info related endpoints

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from fastapi import FastAPI

from openapi_server.apis.v1_internal_api import router as V1InternalApiRouter
from openapi_server.apis.v1_public_api import router as V1PublicApiRouter

app = FastAPI(
    title="UsersAPI",
    description="Microservice that manages authentication and user info related endpoints",
    version="1.0.0",
)

app.include_router(V1InternalApiRouter)
app.include_router(V1PublicApiRouter)
