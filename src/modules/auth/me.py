from datetime import datetime

from core.helpers.jwt_token import JWToken
from core.database.database import Database
from core.schemas.http import HTTPRequest, HTTPResponse
from core.database.repositories.user.repo import UserRepo
from core.schemas.login import LoginRequest, LoginResponse, MeResponse
from core.helpers.errors import HttpException, error_handler


class UseCase:
    def __init__(self):
        database = Database()
        self.user_repo = UserRepo(database)

    def __call__(self, access_token: str) -> MeResponse:
        username = JWToken.decode(access_token)
        if not username:
            raise HttpException(status_code=401, message="Token inválido ou expirado!")

        user = self.user_repo.get_user_by_email(username)

        return MeResponse(
            name=user.name,
            email=user.email,
            created_at=datetime.strftime(user.created_at, "%d/%m/%Y %H:%M:%S")
        )


@error_handler
def lambda_handler(event, context):
    request = HTTPRequest(event)
    access_token = request.headers.get("Authorization")

    use_case = UseCase()
    response = use_case(access_token)

    http_response = HTTPResponse(
        status_code=200,
        body=response.model_dump(),
        message="Login realizado com sucesso!"
    )

    return http_response.to_dict()
