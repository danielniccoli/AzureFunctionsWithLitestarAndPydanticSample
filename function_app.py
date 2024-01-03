from typing import Annotated

import azure.functions as func
from litestar import Litestar, post
from litestar.contrib.pydantic import PydanticPlugin
from litestar.params import Parameter

from models import SecurityGroupRequest


@post("/securitygroup")
async def securitygroup_post(
    data: SecurityGroupRequest,
    x_ms_client_principal_id: Annotated[
        str, Parameter(header="x-ms-client-principal-id")
    ],
    x_ms_client_principal_name: Annotated[
        str, Parameter(header="x-ms-client-principal-name")
    ],
) -> SecurityGroupRequest:
    # Populate the model's internal properties
    data._requestor = (x_ms_client_principal_id, x_ms_client_principal_name)
    return data


pydantic_plugin = PydanticPlugin(prefer_alias=True)
litestar_app = Litestar([securitygroup_post], plugins=[pydantic_plugin])
app = func.AsgiFunctionApp(app=litestar_app, http_auth_level=func.AuthLevel.ANONYMOUS)
