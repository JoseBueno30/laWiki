# coding: utf-8

"""
    laWiki API Gateway

    The Articles API provides endpoints for managing and retrieving articles and article versions within the wiki application. It supports core CRUD (Create, Read, Update, Delete) operations, search functionality, and versioning.

    The version of the OpenAPI document: 1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json




from datetime import date
from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List
from openapi_server.models.author import Author
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class Comment(BaseModel):
    """
    Comment entity response
    """ # noqa: E501
    id: StrictStr = Field(description="The unique ID of the comment")
    article_id: StrictStr = Field(description="The unique ID of the article")
    author: Author
    body: StrictStr = Field(description="The content of the comment")
    creation_date: date = Field(description="The date of creation of the comment")
    __properties: ClassVar[List[str]] = ["id", "article_id", "author", "body", "creation_date"]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of Comment from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={
            },
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of author
        if self.author:
            _dict['author'] = self.author.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of Comment from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "article_id": obj.get("article_id"),
            "author": Author.from_dict(obj.get("author")) if obj.get("author") is not None else None,
            "body": obj.get("body"),
            "creation_date": obj.get("creation_date")
        })
        return _obj

