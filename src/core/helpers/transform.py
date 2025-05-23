from decimal import Decimal

from fastapi import Request
from typing import Dict, Any, Optional


async def fastapi_request_to_lambda_event(
        request: Request,
        body_override: str = None,
        token: Optional[str] = None,
) -> Dict[str, Any]:
    if body_override is not None:
        body_str = body_override
    else:
        body_bytes = await request.body()
        try:
            body_str = body_bytes.decode("utf-8")
        except UnicodeDecodeError:
            body_str = ""

    headers = {
        "Content-Type": request.headers.get("Content-Type", "application/json"),
        "X-Amz-Date": request.headers.get("X-Amz-Date", ""),
        "X-Amz-Security-Token": request.headers.get("X-Amz-Security-Token", ""),
        "Authorization": token if token else request.headers.get("Authorization", ""),
    }

    return {
        "httpMethod": request.method,
        "headers": headers,
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


def decimal_to_number(value: Any) -> Any:
    if isinstance(value, Decimal):
        return float(value) if value % 1 else int(value)
    elif isinstance(value, list):
        return [decimal_to_number(item) for item in value]
    elif isinstance(value, dict):
        return {key: decimal_to_number(val) for key, val in value.items()}
    else:
        return value
