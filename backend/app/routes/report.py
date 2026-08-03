from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app import crud

from app.schemas.report import ReportCreate, ReportResponse
from app.services.scanner import scan_nvd

router = APIRouter(prefix="/reports", tags=["Reports"])

# Sync the NVD security reports to this database.
@router.post("/sync-nvd")
def sync_nvd(
    domain: str | None = None,
    days_back: int = 30,
    mode: str = "modified",
    db: Session = Depends(get_db),
):
    result = scan_nvd(
        db,
        domain=domain,
        days_back=days_back,
        mode=mode
    )

    if result is None:
        raise HTTPException(
            status_code=404, 
            detail="Company not found."
        )

    return result

# Create a report.
@router.post("/{company_id}", response_model=ReportResponse)
def create_report(company_id: int, report: ReportCreate, db: Session = Depends(get_db)):
    return crud.create_report(db, company_id, report)

# Get the reports of security incidents.
@router.get("", response_model=list[ReportResponse] | ReportResponse)
def get_reports(
    db: Session = Depends(get_db),
    company_id: int | None = None, 
    domain: str | None = None,
    limit: int | None = None,
    offset: int | None = None):

    # Ensure the user has entered a company name and offset if they specify a limit.
    if limit is not None and (offset is None) and (company_id is not None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Specify an offset if you wish to set a limit (e.g.: 0)."
        )
    
    # Search for reports within the given
    reports = crud.get_reports(
        db, 
        company_id=company_id, 
        domain=domain,
        limit=limit,
        offset=offset
    )

    # No reports found.
    if not reports:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Report not found."
        )
    
    return reports

