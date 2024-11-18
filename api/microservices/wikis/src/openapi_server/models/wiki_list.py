# coding: utf-8

"""
    Wiki API

    This API is used to perform operations on the wikis of laWiki

    The version of the OpenAPI document: 2.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json




from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from openapi_server.models.simplified_wiki import SimplifiedWiki
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class WikiList(BaseModel):
    """
    List of Wikis. Supports pagination.
    """ # noqa: E501
    articles: List[SimplifiedWiki]
    total: StrictInt = Field(description="The total number of items available to return.")
    offset: StrictInt = Field(description="The offset of the items returned (as set in the query or by default)")
    limit: Annotated[int, Field(strict=True, ge=0)] = Field(description="The maximum number of items in the response (as set in the query or by default).")
    previous: Optional[StrictStr] = Field(description="Request to the previous page of items. ( null if none)")
    next: Optional[StrictStr] = Field(description="Request to the next page of items. ( null if none) ")
    __properties: ClassVar[List[str]] = ["articles", "total", "offset", "limit", "previous", "next"]

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
        """Create an instance of WikiList from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in articles (list)
        _items = []
        if self.articles:
            for _item in self.articles:
                if _item:
                    _items.append(_item.to_dict())
            _dict['articles'] = _items
        # set to None if previous (nullable) is None
        # and model_fields_set contains the field
        if self.previous is None and "previous" in self.model_fields_set:
            _dict['previous'] = None

        # set to None if next (nullable) is None
        # and model_fields_set contains the field
        if self.next is None and "next" in self.model_fields_set:
            _dict['next'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of WikiList from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "articles": [SimplifiedWiki.from_dict(_item) for _item in obj.get("articles")] if obj.get("articles") is not None else None,
            "total": obj.get("total"),
            "offset": obj.get("offset"),
            "limit": obj.get("limit"),
            "previous": obj.get("previous"),
            "next": obj.get("next")
        })
        return _obj


