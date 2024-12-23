# coding: utf-8

"""
    ArticlesAPI

    The Articles API provides endpoints for managing and retrieving articles and article versions within the wiki application. It supports core CRUD (Create, Read, Update, Delete) operations, search functionality, and versioning.

    The version of the OpenAPI document: 3.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json




from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List
from openapi_server.models.tag_v1 import TagV1
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class IdTagsBodyV1(BaseModel):
    """
    IdTagsBodyV1
    """ # noqa: E501
    tag_ids: List[TagV1] = Field(description="List of Tag IDs")
    __properties: ClassVar[List[str]] = ["tag_ids"]

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
        """Create an instance of IdTagsBodyV1 from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in tag_ids (list)
        _items = []
        if self.tag_ids:
            for _item in self.tag_ids:
                if _item:
                    _items.append(_item.to_dict())
            _dict['tag_ids'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of IdTagsBodyV1 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "tag_ids": [TagV1.from_dict(_item) for _item in obj.get("tag_ids")] if obj.get("tag_ids") is not None else None
        })
        return _obj


