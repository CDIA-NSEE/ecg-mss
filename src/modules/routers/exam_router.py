import json

from fastapi import APIRouter, Request, Depends, HTTPException

from modules.routers.auth_router import oauth2_scheme
from modules.exams.next_ecg_exam import lambda_handler as next_ecg_exam_lambda_handler
from modules.exams.create_ecg_report import lambda_handler as create_ecg_report_lambda_handler

from core.schemas.exam import EcgReportRequest
from core.helpers.transform import fastapi_request_to_lambda_event

exam_router = APIRouter(prefix="/exams", tags=["Exams"])


@exam_router.post(
    "/ecg/report",
    summary="Create ECG Report",
    description="Create a new ECG report for an exam",
    response_model=dict
)
async def create_ecg_report(
        request: Request,
        ecg_report: EcgReportRequest,
        token: str = Depends(oauth2_scheme),
):
    """
    Create ECG report endpoint.
    """
    event = await fastapi_request_to_lambda_event(
        request=request,
        token=token,
    )
    response = create_ecg_report_lambda_handler(event, None)

    if response["statusCode"] != 200:
        raise HTTPException(
            status_code=response["statusCode"],
            detail=json.loads(response["body"]).get("details", "An error occurred")
        )

    body = json.loads(response["body"])
    return body


@exam_router.get(
    "/ecg/next",
    summary="Get Next ECG Exam",
    description="Get the next ECG exam that requires reporting",
    response_model=dict
)
async def get_next_ecg_exam(
        request: Request,
        token: str = Depends(oauth2_scheme),
):
    """
    Get next ECG exam endpoint.
    """
    event = await fastapi_request_to_lambda_event(
        request=request,
        token=token,
    )
    response = next_ecg_exam_lambda_handler(event, None)

    if response["statusCode"] != 200:
        raise HTTPException(
            status_code=response["statusCode"],
            detail=json.loads(response["body"]).get("details", "An error occurred")
        )

    body = json.loads(response["body"])
    return body
