import json
from fastapi.openapi.utils import get_openapi

from api_servers.server import app


def get_openapi_json():
    openapi_schema = get_openapi(
        title=app.title,
        summary=app.summary,
        version=app.version,
        description=app.description,
        servers=app.servers,
        routes=app.routes,
    )
    return openapi_schema


if __name__ == "__main__":
    openapi_spec = get_openapi_json()

    with open("../../resources/apis/essentials_openapi.json", "w") as f:
        json.dump(openapi_spec, f, indent=2)

    print("OpenAPI spec written to openapi.json")
