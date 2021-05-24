import json
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Literal, Mapping, Optional, Union

from lxml import etree
from pydantic import BaseModel as PydanticBaseModel, Field
from pydantic.class_validators import ROOT_KEY
from pydantic.utils import to_camel
from pydantic.validators import str_validator


class BaseModel(PydanticBaseModel):
    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        return data[ROOT_KEY] if self.__custom_root_type__ else data


def decapitalize(string: str):
    if not string:
        return string
    return string[0].lower() + string[1:]


def to_lower_camel(string: str):
    camel = to_camel(string)
    return decapitalize(camel)


class XmlString(str):
    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(type='string', contentMediaType='application/xml')

    @classmethod
    def __get_validators__(cls) -> 'CallableGenerator':
        yield str_validator
        yield cls.validate

    @classmethod
    def validate(cls, value: Union[str]) -> str:
        try:
            etree.parse(value)
        except:
            raise ValueError("Is not a valid XML.")
        return value


class JsonString(str):
    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(type='string', format='json-string')

    @classmethod
    def __get_validators__(cls) -> 'CallableGenerator':
        yield cls.validate

    @classmethod
    def validate(cls, value: Union[str, Any]) -> str:
        try:
            if isinstance(value, str):
                json.loads(value)
            else:
                value = json.dumps(value)
        except:
            raise ValueError("Is not a valid JSON.")
        return value


class VariableTypes(str, Enum):
    boolean = "Boolean"
    bytes = "Bytes"
    short = "Short"
    integer = "Integer"
    long = "Long"
    double = "Double"
    date = "Date"
    string = "String"
    null = "Null"

    file = "File"

    object = "Object"

    json = "Json"
    xml = "Xml"


class Boolean(BaseModel):
    type: Literal[VariableTypes.boolean.value] = Field(...)
    value: Optional[bool]
    value_info: Optional[Any] = Field(None)

    class Config:
        alias_generator = to_lower_camel


class Bytes(BaseModel):
    type: Literal[VariableTypes.bytes.value] = Field(...)
    value: Optional[bytes]
    value_info: Optional[Any] = Field(None)

    class Config:
        alias_generator = to_lower_camel


class Short(BaseModel):
    type: Literal[VariableTypes.short.value] = Field(...)
    value: Optional[int]
    value_info: Optional[Any] = Field(None)

    class Config:
        alias_generator = to_lower_camel


class Integer(BaseModel):
    type: Literal[VariableTypes.integer.value] = Field(...)
    value: Optional[int]
    value_info: Optional[Any] = Field(None)

    class Config:
        alias_generator = to_lower_camel


class Long(BaseModel):
    type: Literal[VariableTypes.long.value] = Field(...)
    value: Optional[int]
    value_info: Optional[Any] = Field(None)

    class Config:
        alias_generator = to_lower_camel


class Double(BaseModel):
    type: Literal[VariableTypes.double.value] = Field(...)
    value: Optional[float]
    value_info: Optional[Any] = Field(None)

    class Config:
        alias_generator = to_lower_camel


class Date(BaseModel):
    type: Literal[VariableTypes.date.value] = Field(...)
    value: Optional[datetime]
    value_info: Optional[Any] = Field(None)

    class Config:
        alias_generator = to_lower_camel


class String(BaseModel):
    type: Literal[VariableTypes.string.value] = Field(...)
    value: Optional[str]
    value_info: Optional[Any] = Field(None)

    class Config:
        alias_generator = to_lower_camel


class Null(BaseModel):
    type: Literal[VariableTypes.null.value] = Field(...)
    value: Literal[None]
    value_info: Optional[Any] = Field(None)

    class Config:
        alias_generator = to_lower_camel


class Object(BaseModel):
    type: Literal[VariableTypes.object.value] = Field(...)
    value: Optional[Any]
    value_info: Optional[Any] = Field(None)

    class Config:
        alias_generator = to_lower_camel


class Json(BaseModel):
    type: Literal[VariableTypes.json.value] = Field(...)
    value: Optional[JsonString]
    value_info: Optional[Any] = Field(None)

    class Config:
        alias_generator = to_lower_camel


class Xml(BaseModel):
    type: Literal[VariableTypes.xml.value] = Field(...)
    value: Optional[XmlString]
    value_info: Optional[Any] = Field(None)

    class Config:
        alias_generator = to_lower_camel


VariableValueDto = Union[Boolean, Bytes, Short, Integer, Long, Double, Date, String, Null, Object, Json, Xml]
VariableValues = Mapping[str, VariableValueDto]
