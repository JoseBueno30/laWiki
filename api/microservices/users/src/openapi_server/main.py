# coding: utf-8

"""
    UsersAPI

    Microservice that manages authentication and user info related endpoints

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from fastapi import FastAPI
import firebase_admin
from firebase_admin import credentials
from starlette.middleware.cors import CORSMiddleware

from openapi_server.apis.v1_internal_api import router as V1InternalApiRouter
from openapi_server.apis.v1_public_api import router as V1PublicApiRouter

app = FastAPI(
    title="UsersAPI",
    description="Microservice that manages authentication and user info related endpoints",
    version="1.0.0",
)

cred = credentials.Certificate("./firebase-admin.json")
firebase_admin.initialize_app(cred)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las orígenes, puedes especificar una lista de orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)

app.include_router(V1InternalApiRouter)
app.include_router(V1PublicApiRouter)
