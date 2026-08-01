from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app import crud
from app.schemas.company import CompanyCreate, CompanyResponse

router = APIRouter(prefix="/companies", tags=["Companies"])

# Create a company.
@router.post("", response_model=CompanyResponse)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    return crud.create_company(db, company)

# Search for a company by name or domain (e.g.: ?domain=google.com&name=google) or return all.
@router.get("", response_model=list[CompanyResponse] | CompanyResponse | None)
def get_companies(
    db: Session = Depends(get_db), 
    name: str | None = None, 
    domain: str | None = None):
    
    company = crud.get_companies(db, name=name, domain=domain)

    # No company found.
    if not company:
        raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Company not found."
        )

    return company