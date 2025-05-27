from typing import Optional, List

from pydantic import BaseModel

from core.entities import ReportType, EcgReportSegmentation


class EcgReportRequest(BaseModel):
    exam_id: str
    report_id: Optional[str] = None
    report: Optional[ReportType] = None
    report_segmentation: Optional[EcgReportSegmentation] = None
