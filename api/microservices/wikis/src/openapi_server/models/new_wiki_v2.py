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




from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class NewWikiV2(BaseModel):
    """
    Model of a new wiki
    """ # noqa: E501
    name: Dict[str, StrictStr] = Field(description="Name of the wiki in different languages.")
    description: StrictStr = Field(description="Details of the wiki set by its editors.")
    author: StrictStr = Field(description="Creator of the wiki. Should not remain a string.")
    lang: StrictStr = Field(description="Language of the wiki.")
    image: StrictStr = Field(description="Link to the wiki banner image.")
    translate: bool = Field(description="Indicates if the Wiki shall be translated to the supported languages.")
    __properties: ClassVar[List[str]] = ["name", "description", "author", "lang", "image","translate"]

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
        """Create an instance of NewWikiV2 from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of NewWikiV2 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "description": obj.get("description"),
            "author": obj.get("author"),
            "lang": obj.get("lang"),
            "image": obj.get("image"),
            "translate": obj.get("translate")
        })
        return _obj


