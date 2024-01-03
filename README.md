# Azure Functions with LiteStar and Pydantic integration

This serves as a sample demonstrating the integration of LiteStar and Pydantic into Azure Functions.

LiteStar includes built-in Pydantic support, offering features such as OpenAPI support with Swagger UI and ReDoc UI, as well as data validation using Pydantic, which incorporates JSON schema and provides JSON schema validation.

# Installation

1. Clone this repository
2. Create a Python 3.11 venv at `./.venv`

# Sample HTTP Requests

The following PowerShell snippet sends a valid request to the API. LiteStar will parse and validate the JSON content in the body against the JSON schema of the Pydantic model.

```PowerShell
$paramsSuccess = @{
    Method = "POST"
    Uri = "http://localhost:7071/securitygroup"
    Headers = @{
        "X-MS-CLIENT-PRINCIPAL-NAME"="jon.doe@example.com"
        "X-MS-CLIENT-PRINCIPAL-ID"="eb2f63e0-6344-4bf3-b19b-274fec760547"
    }
    ContentType = "application/json"
    Body = @{
        "owner"="diego.siciliani@example.com"
        "deputy"="ffa69a95-0c0f-4ecf-9d1b-28071a742010"
        "displayName"="Finance Team"
        "description"="Employees working in the finance department."
        "mailEnabled"=$true
    } | ConvertTo-Json

}
Invoke-RestMethod @paramsSuccess
```

The following PowerShell snippet sends an invalid request to the API. LiteStar will parse and validate the JSON content in the body against the JSON schema of the Pydantic model. The model and consequently the JSON schema requires the properties `owner` and `deputy`, which are missing in the request.

```PowerShell
$paramsFails = @{
    Method = "POST"
    Uri = "http://localhost:7071/securitygroup"
    Headers = @{
        "X-MS-CLIENT-PRINCIPAL-NAME"="jon.doe@example.com"
        "X-MS-CLIENT-PRINCIPAL-ID"="eb2f63e0-6344-4bf3-b19b-274fec760547"
    }
    ContentType = "application/json"
    Body = @{
        "displayName"="Finance Team"
        "description"="Employees working in the finance department."
        "mailEnabled"=$true
    } | ConvertTo-Json

}
Invoke-RestMethod @paramsFails
```

Once sent, the API returns the following error message:

```json
{
    "status_code": 400,
    "detail": "Validation failed for POST https://localhost:7071/securitygroup",
    "extra": [
        {"message": "Field required", "key": "owner"},
        {"message": "Field required", "key": "deputy"}
    ]
}
```

> :bulb: You can also check out the automatically generated OpenAPI-based documentation at:
> * `http://localhost:7071/schema` (for [ReDoc](https://redocly.com/redoc)),
> * `http://localhost:7071/schema/swagger` (for [Swagger UI](https://swagger.io/)),
> * `http://localhost:7071/schema/elements` (for [Stoplight Elements](https://stoplight.io/open-source/elements/)),
> * `http://localhost:7071/schema/rapidoc` (for [RapiDoc](https://rapidocweb.com/)),

## Notes

The properties of this sample's Pydantic model `SecurityGroupRequest` adhere to Python's snake case convention. When serializing, Pydantic translates property names directly into JSON on a one-to-one basis. For this sample, we want Pydantic to convert property names to camel case. We can achieve this by passing `by_alias=True`. Since LiteStar handles this behavior, we must instead configure the Pydantic plugin with `prefer_alias=True` as shown below:

```python
pydantic_plugin = PydanticPlugin(prefer_alias=True)
litestar_app = Litestar([securitygroup_post], plugins=[pydantic_plugin])
```

If the property names should be passed "as-is", then this would suffice:

```python
litestar_app = Litestar([securitygroup_post])
```
