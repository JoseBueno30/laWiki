# coding: utf-8

"""
    UsersAPI

    Microservice that manages authentication and user info related endpoints

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json




from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List
from openapi_server.models.user_info import UserInfo
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class VerifyResponse(BaseModel):
    """
    Info obtained retrieved by the oath token
    """ # noqa: E501
    auth_token: StrictStr
    iat_date: StrictInt = Field(description="\"Issued at Time\" in Epoch format")
    exp_date: StrictInt = Field(description="\"Expiration date\" in Epoch format")
    user_info: UserInfo
    __properties: ClassVar[List[str]] = ["auth_token", "iat_date", "exp_date", "user_info"]

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
        """Create an instance of VerifyResponse from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of user_info
        if self.user_info:
            _dict['user_info'] = self.user_info.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of VerifyResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "auth_token": obj.get("auth_token"),
            "iat_date": obj.get("iat_date"),
            "exp_date": obj.get("exp_date"),
            "user_info": UserInfo.from_dict(obj.get("user_info")) if obj.get("user_info") is not None else None
        })
        return _obj


