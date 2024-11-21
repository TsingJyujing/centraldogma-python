from dataclasses import field
from datetime import datetime
from typing import Optional

from dataclasses_json import LetterCase, config, dataclass_json
from dateutil import parser
from marshmallow import fields
from pydantic.dataclasses import dataclass


@dataclass_json
@dataclass
class Creation:
    user: str
    timestamp: Optional[datetime] = field(
        default=None,
        metadata=config(
            decoder=lambda x: parser.parse(x) if x else None,
            mm_field=fields.DateTime(format="iso"),
        ),
    )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class CreatedToken:
    app_id: str
    secret: str
    admin: bool
    creation: Creation


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Token:
    app_id: str
    admin: bool
    creation: Creation
