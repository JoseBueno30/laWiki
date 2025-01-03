# coding: utf-8

"""
    ArticlesAPI

    The Articles API provides endpoints for managing and retrieving articles and article versions within the wiki application. It supports core CRUD (Create, Read, Update, Delete) operations, search functionality, and versioning.

    The version of the OpenAPI document: 2.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json




from datetime import datetime
from pydantic import BaseModel, Field, StrictStr
from typing import Any, ClassVar, Dict, List
from openapi_server.models.models_v1.author_v1 import AuthorV1
from openapi_server.models.models_v1.tag_v1 import TagV1
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class ArticleVersionV1(BaseModel):
    """
    Concrete version of an Article object 
    """ # noqa: E501
    id: StrictStr = Field(description="The ID of the version of the article.")
    article_id: StrictStr = Field(description="The ID of the article.")
    author: AuthorV1
    title: StrictStr = Field(description="The title of the version of the article.")
    modification_date: datetime = Field(description="The date of modification the article that created the version.")
    body: StrictStr = Field(description="The body of the version.")
    tags: List[TagV1] = Field(description="Array of the tags of the version of the article.")
    __properties: ClassVar[List[str]] = ["id", "article_id", "author", "title", "modification_date", "body", "tags"]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
        "extra":  "ignore"
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
        """Create an instance of ArticleVersionV1 from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in tags (list)
        _items = []
        if self.tags:
            for _item in self.tags:
                if _item:
                    _items.append(_item.to_dict())
            _dict['tags'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of ArticleVersionV1 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "article_id": obj.get("article_id"),
            "author": AuthorV1.from_dict(obj.get("author")) if obj.get("author") is not None else None,
            "title": obj.get("title"),
            "modification_date": obj.get("modification_date"),
            "body": obj.get("body"),
            "tags": [TagV1.from_dict(_item) for _item in obj.get("tags")] if obj.get("tags") is not None else None
        })
        return _obj


