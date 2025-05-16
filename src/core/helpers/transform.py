from fastapi import Request
from typing import Dict, Any


async def fastapi_request_to_lambda_event(request: Request) -> Dict[str, Any]:
    body_bytes = await request.body()
    try:
        body_str = body_bytes.decode("utf-8")
    except UnicodeDecodeError:
        body_str = ""

    return {
        "httpMethod": request.method,
        "headers": dict(request.headers),
        "queryStringParameters": dict(request.query_params),
        "pathParameters": request.path_params,
        "body": body_str,
        "isBase64Encoded": False,
        "requestContext": {
            "resourcePath": request.url.path,
            "httpMethod": request.method,
        },
        "path": request.url.path
    }
