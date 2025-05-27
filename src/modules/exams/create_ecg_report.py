from datetime import datetime

from core.helpers.jwt_token import JWToken
from core.helpers.errors import HttpException, error_handler

from core.entities import EcgReport, ReportType

from core.schemas.exam import EcgReportRequest
from core.schemas.http import HTTPRequest, HTTPResponse

from core.database.database import Database
from core.database.repositories.user.repo import UserRepo
from core.database.repositories.exams.repo import ExamRepo


class UseCase:
    def __init__(self):
        database = Database()
        self.user_repo = UserRepo(database)
        self.exam_repo = ExamRepo(database)

    def __call__(self, access_token: str, request: EcgReportRequest):
        username = JWToken.decode(access_token)
        if not username:
            raise HttpException(status_code=401, message="Token inválido ou expirado!")
        user = self.user_repo.get_user_by_email(username)
        if not user:
            raise HttpException(status_code=401, message="Token inválido ou expirado!")

        exam = self.exam_repo.get_exam_by_id(request.exam_id)
        if not exam:
            raise HttpException(status_code=422, message="Exame não encontrado!")

        if exam.approved or exam.principal_report:
            raise HttpException(status_code=422, message="Já existe um relatório principal para este exame!")

        if request.report_id:
            report = next((report for report in exam.reports if report.id == request.report_id), None)
            if not report:
                raise HttpException(status_code=422, message="Relatório não encontrado!")
        else:
            report = EcgReport(
                report=ReportType(request.report),
                report_segmentation=request.report_segmentation,
                created_at=datetime.now()
            )
            exam.reports.append(report)

        exam.principal_report = report
        exam.approved = True
        exam.approved_at = datetime.now()

        exam.reporting_started_at = None
        exam.is_reporting = False

        self.exam_repo.update_exam(exam)


@error_handler
def lambda_handler(event, context):
    request = HTTPRequest(event)
    access_token = request.headers.get("Authorization")

    use_case = UseCase()
    use_case(access_token, EcgReportRequest(**request.body))

    http_response = HTTPResponse(
        status_code=200,
        message="Login realizado com sucesso!"
    )

    return http_response.to_dict()
