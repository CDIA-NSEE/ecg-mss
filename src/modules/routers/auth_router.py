import json

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Request, HTTPException, Depends

from modules.auth.me import lambda_handler as me_lambda_handler
from core.helpers.transform import fastapi_request_to_lambda_event
from modules.auth.login import lambda_handler as login_lambda_handler
from core.schemas.login import LoginResponse, LoginRequest, MeResponse

auth_router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@auth_router.post(
    "/login",
    summary="User login",
    description="Login endpoint for user authentication",
    response_model=LoginResponse
)
async def login(
        request: Request,
        form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Login endpoint.
    """
    body_json = json.dumps({
        "username": form_data.username,
        "password": form_data.password
    })

    event = await fastapi_request_to_lambda_event(request, body_override=body_json)
    response = login_lambda_handler(event, None)

    if response["statusCode"] != 200:
        raise HTTPException(
            status_code=response["statusCode"],
            detail=json.loads(response["body"]).get("details", "An error occurred")
        )

    body = json.loads(response["body"])
    login_response = LoginResponse(**body)

    return login_response


@auth_router.get(
    "/me",
    summary="Get current user",
    description="Get current user information",
    response_model=MeResponse
)
async def get_current_user(
        request: Request,
        token: str = Depends(oauth2_scheme)
):
    """
    Get current user endpoint.
    """
    event = await fastapi_request_to_lambda_event(request, token=token)
    response = me_lambda_handler(event, None)

    if response["statusCode"] != 200:
        raise HTTPException(
            status_code=response["statusCode"],
            detail=json.loads(response["body"]).get("details", "An error occurred")
        )

    body = json.loads(response["body"])
    me_response = MeResponse(**body)

    return me_response
