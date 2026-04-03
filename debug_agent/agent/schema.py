from pydantic import BaseModel

class FixResponse(BaseModel):
    reason: str
    file: str
    fixed_code: str