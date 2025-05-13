from enum import Enum
from typing import List, Optional, Literal

from pydantic import BaseModel, Field
from datetime import datetime, UTC


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
    male = "Masculino"
    female = "Feminino"
    other = "Outro"


class User(BaseModel):
    name: str
    email: str
    password: str
    created_at: datetime = datetime.now(UTC)


class EcgReportStatus(BaseModel):
    status: bool
    created_at: datetime = datetime.now(UTC)
    created_by: User


class EcgReportSegmentation(BaseModel):
    category: ReportSegmentationType
    segmentation: List[List[float]]  # lista de coordenadas do polígono [[x1, y1, x2, y2, ...]]
    bbox: List[float]  # caixa delimitadora [x_min, y_min, width, height]
    area: float  # área da segmentação
    iscrowd: Literal[0, 1] = 0  # se a anotação representa uma multidão (padrão: 0)
    created_at: datetime


class EcgReport(BaseModel):
    report: ReportType
    report_segmentation: Optional[EcgReportSegmentation] = None

    created_at: datetime = datetime.now(UTC)
    created_by: User

    approves: List[EcgReportStatus] = []


class EcgExam(BaseModel):
    id: str
    file_path: str
    made_at: datetime
    gender: Gender
    birth_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    amplitude: str
    speed: str

    principal_report: EcgReport
    reports: List[EcgReport] = []
