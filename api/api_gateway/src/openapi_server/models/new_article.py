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




from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from openapi_server.models.author import Author
from openapi_server.models.tag import Tag
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class NewArticle(BaseModel):
    """
    Data required to the user to create a new Article and its first version
    """ # noqa: E501
    title: StrictStr = Field(description="The title of the version of the article.")
    author: Author
    tags: List[Tag]
    body: Optional[StrictStr] = Field(default=None, description="The body of the version.")
    wiki_id: StrictStr = Field(description="The ID of the Wiki where the Article is created.")
    lan: StrictStr = Field(description="Original language of the first ArticleVersion of the Article")
    trasnlate_title: StrictBool = Field(description="Indicates if the title of the ArticleVersion of the Artivle should be translated in the different translations of the ArticleVersion")
    __properties: ClassVar[List[str]] = ["title", "author", "tags", "body", "wiki_id", "lan", "trasnlate_title"]

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
        """Create an instance of NewArticle from a JSON string"""
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
        """Create an instance of NewArticle from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "title": obj.get("title"),
            "author": Author.from_dict(obj.get("author")) if obj.get("author") is not None else None,
            "tags": [Tag.from_dict(_item) for _item in obj.get("tags")] if obj.get("tags") is not None else None,
            "body": obj.get("body"),
            "wiki_id": obj.get("wiki_id"),
            "lan": obj.get("lan"),
            "trasnlate_title": obj.get("trasnlate_title") if obj.get("trasnlate_title") is not None else True
        })
        return _obj


