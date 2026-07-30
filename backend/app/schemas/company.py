from pydantic import BaseModel

# Used by the API to describe an object it recieved or sent as a company.
# In a request to add a company.
class CompanyCreate(BaseModel):
    name: str
    domain: str

# In a reponse which includes a company.
class CompanyResponse(BaseModel):
    id: int
    name: str
    domain: str
    trust_score: int
    rating: str

    model_config = {
        "from_attributes": True
    }