# coding: utf-8

"""
    Wiki API

    This API is used to perform operations on the wikis of laWiki

    The version of the OpenAPI document: 2.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
from datetime import datetime
import pprint
import re  # noqa: F401
import json




from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Union
from typing_extensions import Annotated
from openapi_server.models.author import Author
from openapi_server.models.tag import Tag
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class Wiki(BaseModel):
    """
    Wiki
    """ # noqa: E501
    id: StrictStr = Field(description="Unique identifier for the wiki.")
    name: StrictStr = Field(description="Name of the wiki.")
    description: StrictStr = Field(description="Details of the wiki set by its editors.")
    creation_date: datetime = Field(description="Date of creation of the wiki.")
    author: Author
    tags: List[Tag]
    rating: Union[Annotated[float, Field(le=5, strict=True, ge=0)], Annotated[int, Field(le=5, strict=True, ge=0)]] = Field(description="Average rating of the wiki")
    __properties: ClassVar[List[str]] = ["id", "name", "description", "creation_date", "author", "tags", "rating"]

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
        """Create an instance of Wiki from a JSON string"""
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
        """Create an instance of Wiki from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "description": obj.get("description"),
            "creation_date": obj.get("creation_date"),
            "author": Author.from_dict(obj.get("author")) if obj.get("author") is not None else None,
            "tags": [Tag.from_dict(_item) for _item in obj.get("tags")] if obj.get("tags") is not None else None,
            "rating": obj.get("rating")
        })
        return _obj

