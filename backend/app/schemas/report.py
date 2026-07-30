from datetime import date
from pydantic import BaseModel

# Used by the API to describe an object it recieved or sent as a report.
# In a request to add a report.
class ReportCreate(BaseModel):
    title: str
    description: str
    report_date: date
    severity: str
    source: str

# In a response which includes a report.
class ReportResponse(BaseModel):
    id: int
    title: str
    description: str
    report_date: date
    severity: str
    source: str

    model_config = {
        "from_attributes": True
    }
