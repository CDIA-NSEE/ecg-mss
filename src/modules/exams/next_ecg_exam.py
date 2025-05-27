from datetime import datetime

from pytz import UTC

from core.helpers.jwt_token import JWToken
from core.helpers.errors import HttpException, error_handler

from core.schemas.http import HTTPRequest, HTTPResponse

from core.database.database import Database
from core.database.repositories.user.repo import UserRepo
from core.database.repositories.exams.repo import ExamRepo


class UseCase:
    def __init__(self):
        database = Database()
        self.user_repo = UserRepo(database)
        self.exam_repo = ExamRepo(database)

    def __call__(self, access_token: str):
        username = JWToken.decode(access_token)
        if not username:
            raise HttpException(status_code=401, message="Token inválido ou expirado!")
        user = self.user_repo.get_user_by_email(username)
        if not user:
            raise HttpException(status_code=401, message="Token inválido ou expirado!")

        exam = self.exam_repo.get_next_ecg_exam()
        if exam:
            was_reporting = exam.is_reporting

            exam.is_reporting = True
            exam.reporting_started_at = datetime.now(UTC)

            if not was_reporting:
                if not self.exam_repo.update_exam(exam):
                    raise HttpException(status_code=422, message="Não foi possível iniciar o relatório do exame ECG.")

        return {"exam": exam.to_dict() if exam else None}


@error_handler
def lambda_handler(event, context):
    request = HTTPRequest(event)
    access_token = request.headers.get("Authorization")

    use_case = UseCase()
    exam = use_case(access_token)

    http_response = HTTPResponse(
        status_code=200,
        body=exam,
        message="Próximo exame ECG obtido com sucesso!"
    )

    return http_response.to_dict()
