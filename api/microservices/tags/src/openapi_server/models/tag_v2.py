# coding: utf-8

"""
    TagAPI

    API for the tags microservice of laWiki web appplication. It provides all endpoints related to CRUD operatios for wiki tags.

    The version of the OpenAPI document: 2.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json




from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List
from openapi_server.models.article import Article
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class TagV2(BaseModel):
    """
    Tag entity.
    """ # noqa: E501
    id: StrictStr = Field(description="The ID of the tag.")
    tag: StrictStr = Field(description="The name of the tag.")
    wiki_id: StrictStr = Field(description="The ID corresponding to the wiki the tag belongs to.")
    articles: List[Article] = Field(description="Array of articles that have the tag.")
    translations: Dict[str, StrictStr] = Field(description="A dictionary with tag translations to other languages.")
    __properties: ClassVar[List[str]] = ["id", "tag", "wiki_id", "articles", "translations"]

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
        """Create an instance of TagV2 from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of TagV2 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "tag": obj.get("tag"),
            "wiki_id": obj.get("wiki_id"),
            "articles": [Article.from_dict(_item) for _item in obj.get("articles")] if obj.get("articles") is not None else None,
            "translations": obj.get("translations")
        })
        return _obj


