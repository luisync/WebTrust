from sqlalchemy.orm import Session
from app.models.company import Company
from app.scoring.builder import build_evidence
from app.scoring.calculator import calculate_score
from app.scoring.ratings import get_rating

# Update a company's score.
def update_score(db: Session):
    # Get all companies.
    companies = db.query(Company).all()

    if not companies:
        return

    # Calculate the raw scores for every company.
    raw_scores: dict[int, int] = {}
    raw_values: list[int] = []

    for current_company in companies:
        evidence = build_evidence(db, current_company.id)
        raw_score = calculate_score(evidence)

        raw_scores[current_company.id] = raw_score
        raw_values.append(raw_score)

    total = len(raw_values)

    # Convert raw scores into relative scores.
    for current_company in companies:
        raw_score = raw_scores[current_company.id]

        lower_count = sum(1 for value in raw_values if value < raw_score)
        equal_count = sum(1 for value in raw_values if value == raw_score)

        # Percentile-style scoring, the higher the raw score, the higher the relative score.
        relative_score = round(100 * ((lower_count + (0.5 * equal_count)) / total))

        relative_score = max(0, min(relative_score, 100))

        current_company.trust_score = relative_score
        current_company.rating = get_rating(raw_score)

    # Update and refresh the database.
    db.commit()

    for current_company in companies:
        db.refresh(current_company)