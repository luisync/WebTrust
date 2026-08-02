from sqlalchemy.orm import Session
from app.models.company import Company
from app.scoring.builder import build_evidence
from app.scoring.calculator import calculate_score
from app.scoring.ratings import get_rating

# Update a companies score.
def update_score(db: Session, company: Company):
    # Build the evidence change the score.
    evidence = build_evidence(db, company.id)

    # Recalculate the score.
    score = calculate_score(evidence)
    rating = get_rating(score)

    # Subsitute the real value.
    company.trust_score = score
    company.rating = rating

    # Commit the changes to the database.
    db.commit()
    db.refresh(company)

    return company