from fastapi import APIRouter
from database.model import ReportOut, ReportRequest
from database.report_model import ReportGenerator

router = APIRouter()

@router.post('/')
async def get_report(requested_report: ReportRequest) -> ReportOut:
    return ReportGenerator().generate(requested_report.model_dump())