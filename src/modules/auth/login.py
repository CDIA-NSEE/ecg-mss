from core.helpers.jwt_token import JWToken
from core.database.database import Database
from core.schemas.http import HTTPRequest, HTTPResponse
from core.database.repositories.user.repo import UserRepo
from core.schemas.login import LoginRequest, LoginResponse
from core.helpers.errors import HttpException, error_handler


class UseCase:
    def __init__(self):
        database = Database()
        self.user_repo = UserRepo(database)

    def __call__(self, login: LoginRequest) -> LoginResponse:
        username = login.username
        password = login.password

        user = self.user_repo.get_user_by_email(username)
        if not user or user.password != password:
            raise HttpException(status_code=403, message="E-mail ou Senha estão incorretos, por favor tente novamente!")

        access_token = JWToken.encode(user.email)
        return LoginResponse(access_token=access_token)


@error_handler
def lambda_handler(event, context):
    request = HTTPRequest(event)
    body = LoginRequest(**request.body)

    use_case = UseCase()
    response = use_case(body)

    http_response = HTTPResponse(
        status_code=200,
        body=response.model_dump(),
        message="Login realizado com sucesso!"
    )

    return http_response.to_dict()
