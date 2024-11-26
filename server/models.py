from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    email: str
    password: str

class Investment(BaseModel):
    scheme_name: str
    amount_invested: float
    current_value: float

class Portfolio(BaseModel):
    user_email: str
    investments: List[Investment]
