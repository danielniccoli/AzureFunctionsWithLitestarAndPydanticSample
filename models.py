from uuid import uuid4

from pydantic import (
    BaseModel,
    ConfigDict,
    PrivateAttr,
    StrictBool,
    computed_field,
    constr,
)
from pydantic.alias_generators import to_camel
from pydantic.config import ConfigDict

config = ConfigDict(
    extra="forbid",
    frozen=True,
    hide_input_errors=True,
    validate_assignment=True,
    alias_generator=to_camel,
    populate_by_name=True,
)


class SecurityGroupRequest(BaseModel):
    model_config = config

    # Used to store the requestor. Must be validaten by the business logic
    # and MUST NOT be settable by the requestor!
    _requestor: tuple[str, str] = PrivateAttr()  # Todo: Make a list

    # Required properties for Microsoft Graph API resource type
    display_name: constr(max_length=256)  # type: ignore
    mail_enabled: StrictBool = False
    _mail_nickname = PrivateAttr(default_factory=lambda: str(uuid4())[:10])
    security_enabled: StrictBool = True

    # Required properties for business process
    owner: str
    deputy: str
    description: constr(max_length=1000)  # type: ignore

    @computed_field
    @property
    def mail_nickname(self) -> str:
        return self._mail_nickname
