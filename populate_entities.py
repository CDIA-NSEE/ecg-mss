from decimal import Decimal

from pytz import UTC
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Any


def number_to_decimal(value: Any) -> Any:
    if isinstance(value, (int, float)):
        return Decimal(value)
    elif isinstance(value, list):
        return [number_to_decimal(item) for item in value]
    elif isinstance(value, dict):
        return {key: number_to_decimal(val) for key, val in value.items()}
    else:
        return value


def decimal_to_number(value: Any) -> Any:
    if isinstance(value, Decimal):
        return float(value) if value % 1 else int(value)
    elif isinstance(value, list):
        return [decimal_to_number(item) for item in value]
    elif isinstance(value, dict):
        return {key: decimal_to_number(val) for key, val in value.items()}
    else:
        return value


class ReportType(Enum):
    NORMAL = "ECG normal"
    TAQUICARDIA_SINUSAL = "Taquicardia sinusal"
    BRADICARDIA_SINUSAL = "Bradicardia sinusal"
    ARRITMIA_SINUSAL = "Arritmia sinusal"
    BLOQUEIO_AV_1_GRAU = "Bloqueio atrioventricular de 1º grau"
    BLOQUEIO_AV_2_GRAU_TIPO_1 = "Bloqueio atrioventricular de 2º grau tipo Mobitz I"
    BLOQUEIO_AV_2_GRAU_TIPO_2 = "Bloqueio atrioventricular de 2º grau tipo Mobitz II"
    BLOQUEIO_AV_3_GRAU = "Bloqueio atrioventricular de 3º grau"
    BLOQUEIO_RBBB = "Bloqueio de ramo direito completo"
    BLOQUEIO_LBBB = "Bloqueio de ramo esquerdo completo"
    FIBRILACAO_ATRIAL = "Fibrilação atrial"
    FLUTTER_ATRIAL = "Flutter atrial"
    TAQUICARDIA_SUPRAVENTRICULAR = "Taquicardia supraventricular"
    TAQUICARDIA_VENTRICULAR = "Taquicardia ventricular"
    FIBRILACAO_VENTRICULAR = "Fibrilação ventricular"
    INFARTO_AGUDO_MIOCARDIO = "Infarto agudo do miocárdio"
    ISQUEMIA_SUBENDOCARDICA = "Isquemia subendocárdica"
    HIPERTROFIA_VENTRICULO_ESQUERDO = "Hipertrofia do ventrículo esquerdo"
    HIPERTROFIA_VENTRICULO_DIREITO = "Hipertrofia do ventrículo direito"
    EIXO_DESVIADO_ESQUERDA = "Desvio do eixo elétrico para a esquerda"
    EIXO_DESVIADO_DIREITA = "Desvio do eixo elétrico para a direita"
    ALTERACOES_INESPECIFICAS_ST_T = "Alterações inespecíficas do segmento ST-T"
    PRESENCA_MARCAPASSO = "Presença de marcapasso"
    ECG_INCONCLUSIVO = "ECG inconclusivo"


class ReportSegmentationType(Enum):
    NORMAL = "Normal"
    TAQUICARDIA_SINUSAL = "Taquicardia sinusal"
    BRADICARDIA_SINUSAL = "Bradicardia sinusal"
    ARRITMIA_SINUSAL = "Arritmia sinusal"
    BLOQUEIO_AV_1_GRAU = "Bloqueio atrioventricular de 1º grau"
    BLOQUEIO_AV_2_GRAU_TIPO_1 = "Bloqueio atrioventricular de 2º grau tipo Mobitz I"
    BLOQUEIO_AV_2_GRAU_TIPO_2 = "Bloqueio atrioventricular de 2º grau tipo Mobitz II"
    BLOQUEIO_AV_3_GRAU = "Bloqueio atrioventricular de 3º grau"
    BLOQUEIO_RBBB = "Bloqueio de ramo direito completo"
    BLOQUEIO_LBBB = "Bloqueio de ramo esquerdo completo"
    FIBRILACAO_ATRIAL = "Fibrilação atrial"
    FLUTTER_ATRIAL = "Flutter atrial"
    TAQUICARDIA_SUPRAVENTRICULAR = "Taquicardia supraventricular"
    TAQUICARDIA_VENTRICULAR = "Taquicardia ventricular"
    FIBRILACAO_VENTRICULAR = "Fibrilação ventricular"
    INFARTO_AGUDO_MIOCARDIO = "Infarto agudo do miocárdio"
    ISQUEMIA_SUBENDOCARDICA = "Isquemia subendocárdica"
    HIPERTROFIA_VENTRICULO_ESQUERDO = "Hipertrofia do ventrículo esquerdo"
    HIPERTROFIA_VENTRICULO_DIREITO = "Hipertrofia do ventrículo direito"
    EIXO_DESVIADO_ESQUERDA = "Desvio do eixo elétrico para a esquerda"
    EIXO_DESVIADO_DIREITA = "Desvio do eixo elétrico para a direita"
    ALTERACOES_INESPECIFICAS_ST_T = "Alterações inespecíficas do segmento ST-T"
    PRESENCA_MARCAPASSO = "Presença de marcapasso"


class Gender(Enum):
    MALE = "Masculino"
    FEMALE = "Feminino"
    OTHER = "Outro"


class UserRole(Enum):
    DOCTOR_MANAGER = "doctor_manager"
    DOCTOR = "doctor"


class User(BaseModel):
    name: str
    email: str
    password: str
    role: UserRole
    created_at: datetime = datetime.now(UTC)

    def to_dynamo(self):
        data = {
            "PK": f"USER#{self.email}",
            "SK": self.created_at.timestamp(),
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "role": self.role.value,
            "type": "USER",
        }
        return number_to_decimal(data)

    @classmethod
    def from_dynamo(cls, data: dict) -> "User":
        data = decimal_to_number(data)
        return cls(
            name=data["name"],
            email=data["email"],
            password=data["password"],
            created_at=datetime.fromtimestamp(data["SK"], tz=UTC),
            role=UserRole(data["role"])
        )


class EcgReportStatus(BaseModel):
    status: bool
    created_at: datetime = datetime.now(UTC)
    created_by: User

    def to_dynamo(self):
        data = {
            "status": self.status,
            "created_at": self.created_at.timestamp(),
            "created_by": self.created_by.email,
        }
        return number_to_decimal(data)

    @classmethod
    def from_dynamo(cls, data: dict) -> "EcgReportStatus":
        data = decimal_to_number(data)
        return cls(
            status=data["status"],
            created_at=datetime.fromtimestamp(data["created_at"], tz=UTC),
            created_by=User.from_dynamo(data["created_by"]),
        )


class EcgReportSegmentation(BaseModel):
    category: ReportSegmentationType
    segmentation: List[List[float]]  # lista de coordenadas do polígono [[x1, y1, x2, y2, ...]]
    bbox: List[float]  # caixa delimitadora [x_min, y_min, width, height]
    area: float  # área da segmentação
    iscrowd: Literal[0, 1] = 0  # se a anotação representa uma multidão (padrão: 0)
    created_at: datetime

    def to_dynamo(self):
        data = {
            "category": self.category.value,
            "segmentation": self.segmentation,
            "bbox": self.bbox,
            "area": self.area,
            "iscrowd": self.iscrowd,
            "created_at": self.created_at.timestamp(),
        }
        return number_to_decimal(data)

    @classmethod
    def from_dynamo(cls, data: dict) -> "EcgReportSegmentation":
        data = decimal_to_number(data)
        return cls(
            category=ReportSegmentationType(data["category"]),
            segmentation=data["segmentation"],
            bbox=data["bbox"],
            area=data["area"],
            iscrowd=data["iscrowd"],
            created_at=datetime.fromtimestamp(data["created_at"], tz=UTC),
        )


class EcgReport(BaseModel):
    report: ReportType
    report_segmentation: Optional[EcgReportSegmentation] = None
    created_at: datetime = datetime.now(UTC)

    def to_dynamo(self):
        data = {
            "report": self.report.value,
            "report_segmentation": self.report_segmentation.to_dynamo() if self.report_segmentation else None,
            "created_at": self.created_at.timestamp(),
        }
        return number_to_decimal(data)

    @classmethod
    def from_dynamo(cls, data: dict) -> "EcgReport":
        report_segmentation = (
            EcgReportSegmentation.from_dynamo(data["report_segmentation"])
            if data.get("report_segmentation")
            else None
        )
        data = decimal_to_number(data)
        return cls(
            report=ReportType(data["report"]),
            report_segmentation=report_segmentation,
            created_at=datetime.fromtimestamp(data["created_at"], tz=UTC)
        )


class EcgExam(BaseModel):
    id: str
    file_path: str
    made_at: datetime
    gender: Gender
    birth_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    amplitude: str
    speed: str

    approved: bool = False
    approved_at: Optional[datetime] = None

    is_reporting: bool = False
    reporting_started_at: Optional[datetime] = None

    principal_report: Optional[EcgReport] = None
    reports: List[EcgReport] = []

    def to_dynamo(self):
        data = {
            "PK": f"ECG_EXAM#{self.id}",
            "SK": self.made_at.timestamp(),
            "file_path": self.file_path,
            "gender": self.gender.value,
            "birth_date": self.birth_date,
            "amplitude": self.amplitude,
            "speed": self.speed,
            "approved": self.approved,
            "approved_at": self.approved_at.timestamp() if self.approved_at else None,
            "principal_report": self.principal_report.to_dynamo() if self.principal_report else None,
            "reports": [report.to_dynamo() for report in self.reports],
            "is_reporting": self.is_reporting,
            "reporting_started_at": self.reporting_started_at.timestamp() if self.reporting_started_at else None,
            "type": "ECG_EXAM",
        }
        return number_to_decimal(data)

    @classmethod
    def from_dynamo(cls, data: dict) -> "EcgExam":
        data = decimal_to_number(data)
        return cls(
            id=data["PK"].split("#")[1],
            file_path=data["file_path"],
            made_at=datetime.fromtimestamp(data["SK"], tz=UTC),
            gender=Gender(data["gender"]),
            birth_date=data["birth_date"],
            amplitude=data["amplitude"],
            speed=data["speed"],
            approved=data["approved"],
            approved_at=datetime.fromtimestamp(data["approved_at"], tz=UTC) if data.get("approved_at") else None,
            principal_report=EcgReport.from_dynamo(data["principal_report"]) if data.get("principal_report") else None,
            reports=[EcgReport.from_dynamo(report) for report in data.get("reports", [])],
        )
