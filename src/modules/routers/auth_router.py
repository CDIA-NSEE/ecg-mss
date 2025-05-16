import json

from fastapi import APIRouter, Request, HTTPException

from core.helpers.transform import fastapi_request_to_lambda_event
from core.schemas.login import LoginResponse, LoginRequest
from modules.auth.login import lambda_handler

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post(
    "/login",
    summary="User login",
    description="Login endpoint for user authentication",
    response_model=LoginResponse
)
async def login(
        request: Request,
        body: LoginRequest
):
    """
    Login endpoint.
    """
    event = await fastapi_request_to_lambda_event(request)
    response = lambda_handler(event, None)

    if response["statusCode"] != 200:
        raise HTTPException(
            status_code=response["statusCode"],
            detail=json.loads(response["body"]).get("details", "An error occurred")
        )

    body = json.loads(response["body"])
    login_response = LoginResponse(**body)

    return login_response
