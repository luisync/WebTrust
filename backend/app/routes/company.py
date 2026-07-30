from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app import crud
from app.schemas.company import CompanyCreate, CompanyResponse

router = APIRouter(prefix="/companies", tags=["Companies"])

# Create a company.
@router.post("", response_model=CompanyResponse)
def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db)
):
    return crud.create_company(db, company)

# Get all companies.
@router.get("", response_model=list[CompanyResponse])
def get_companies(
    db: Session = Depends(get_db)
):
    return crud.get_companies(db)


