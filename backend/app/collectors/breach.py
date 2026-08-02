from app.scoring.evidence import CompanyEvidence

# Scans the trusted sources for security breaches.
def collect(domain: str, evidence: CompanyEvidence):
    return evidence