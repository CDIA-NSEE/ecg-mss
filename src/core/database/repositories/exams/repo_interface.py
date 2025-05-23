from abc import abstractmethod
from typing import Optional, Tuple, List

from core.entities import EcgExam, EcgReport


class IExamRepo:
    @abstractmethod
    def get_exam_by_id(self, exam_id: str) -> Optional[EcgExam]:
        """Get exam by ID"""
        pass

    @abstractmethod
    def create_exam(self, exam: EcgExam) -> bool:
        """Create a new exam"""
        pass

    @abstractmethod
    def update_exam(self, exam: EcgExam) -> bool:
        """Update an existing exam"""
        pass

    @abstractmethod
    def delete_exam(self, exam_id: str) -> bool:
        """Delete an exam by ID"""
        pass

    @abstractmethod
    def check_if_exam_is_approved(self, exam_id: str) -> bool:
        """Check if an exam is approved"""
        pass

    @abstractmethod
    def approve_exam(self, exam_id: str, report: EcgReport) -> bool:
        """Approve an exam"""
        pass

    @abstractmethod
    def create_exam_report(self, exam_id: str, report: EcgReport) -> bool:
        """Create a new exam report"""
        pass

    @abstractmethod
    def count_exams(self, approved: Optional[bool] = None, date_range: Optional[Tuple[str, str]] = None) -> int:
        """Count the number of exams"""
        pass

    @abstractmethod
    def get_all_exams(self, limit: int = 10, offset: int = 0, approved: Optional[bool] = None) -> List[EcgExam]:
        """Get all exams with pagination"""
        pass
