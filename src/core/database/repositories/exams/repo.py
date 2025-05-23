from typing import Optional, Tuple, Literal, List

from core.database.database import Database
from core.database.repositories.exams.repo_interface import IExamRepo
from core.entities import EcgExam, EcgReport


class ExamRepo(IExamRepo):
    def __init__(self, db: Database):
        self.db = db
        self.dynamo = db.dynamodb

    def get_exam_by_id(self, exam_id: str) -> Optional[EcgExam]:
        """Get exam by ID"""
        exam = self.dynamo.get_item({"exam_id": exam_id})
        if exam:
            exam = self.db.deserialize(exam)
            return EcgExam.from_dynamo(exam)
        return None

    def create_exam(self, exam: EcgExam) -> bool:
        """Create a new exam"""
        try:
            exam = self.db.serialize(exam.to_dynamo())
            self.dynamo.put_item(exam)
            return True
        except Exception as e:
            print(f"Error creating exam: {e}")
            return False

    def update_exam(self, exam: EcgExam) -> bool:
        """Update an existing exam"""
        try:
            self.dynamo.update_item(
                key={"exam_id": exam.exam_id},
                update_expression="SET #status = :status",
                expression_attribute_names={"#status": "status"},
                expression_attribute_values={":status": exam.status}
            )
            return True
        except Exception as e:
            print(f"Error updating exam: {e}")
            return False

    def delete_exam(self, exam_id: str) -> bool:
        """Delete an exam by ID"""
        try:
            self.dynamo.delete_item({"exam_id": exam_id})
            return True
        except Exception as e:
            print(f"Error deleting exam: {e}")
            return False

    def check_if_exam_is_approved(self, exam_id: str) -> bool:
        """Check if an exam is approved"""
        try:
            exam = self.get_exam_by_id(exam_id)
            return exam.approved if exam else False
        except Exception as e:
            print(f"Error checking if exam is approved: {e}")
            return False

    def approve_exam(self, exam_id: str, report: EcgReport) -> bool:
        """Approve an exam"""
        try:
            exam = self.get_exam_by_id(exam_id)
            if exam:
                exam.approved = True
                exam.principal_report = report
                exam.reports.append(report)
                exam.approved_at = report.created_at
                self.update_exam(exam)
                return True
            return False
        except Exception as e:
            print(f"Error approving exam: {e}")
            return False

    def get_all_exams(
            self,
            limit: int = 10,
            offset: int = 0,
            approved: Optional[bool] = None,
            order_by: Literal["asc", "desc"] = "asc"
    ) -> List[EcgExam]:
        """Get all exams with pagination"""
        try:
            exams = self.dynamo.scan(
                limit=limit,
                exclusive_start_key=offset,
                filter_expression="approved = :approved" if approved else None,
                expression_attribute_values={":approved": approved} if approved else None
            )
            return [EcgExam.from_dynamo(exam) for exam in exams]
        except Exception as e:
            print(f"Error getting all exams: {e}")
            return []

    def count_exams(self, approved: Optional[bool] = None, date_range: Optional[Tuple[str, str]] = None) -> int:
        """Count the number of exams"""
        try:
            filter_expression = None
            expression_attribute_values = {}

            if approved is not None:
                filter_expression = "approved = :approved"
                expression_attribute_values[":approved"] = approved

            if date_range:
                start_date, end_date = date_range
                filter_expression += " AND made_at BETWEEN :start_date AND :end_date"
                expression_attribute_values[":start_date"] = start_date
                expression_attribute_values[":end_date"] = end_date

            count = self.dynamo.scan(
                filter_expression=filter_expression,
                expression_attribute_values=expression_attribute_values
            )
            return count
        except Exception as e:
            print(f"Error counting exams: {e}")
            return 0

    def create_exam_report(self, exam_id: str, report: EcgReport) -> bool:
        """Create a new exam report"""
        try:
            exam = self.get_exam_by_id(exam_id)
            if exam:
                exam.reports.append(report)
                self.update_exam(exam)
                return True
            return False
        except Exception as e:
            print(f"Error creating exam report: {e}")
            return False
