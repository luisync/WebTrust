from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app import crud

from app.schemas.report import ReportCreate, ReportResponse

router = APIRouter(prefix="/reports", tags=["Reports"])

# Create a report.
@router.post("/{company_id}", response_model=ReportResponse)
def create_report(
    company_id: int,
    report: ReportCreate,
    db: Session = Depends(get_db)
):
    return crud.create_report(db, company_id, report)

# Get all reports.
@router.get("", response_model=list[ReportResponse])
def get_reports(
    db: Session = Depends(get_db)
):
    return crud.get_reports(db)