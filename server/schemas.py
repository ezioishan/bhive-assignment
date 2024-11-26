from pydantic import BaseModel, EmailStr
from typing import List

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class InvestmentResponse(BaseModel):
    scheme_name: str
    amount_invested: float
    current_value: float

class PortfolioResponse(BaseModel):
    user_email: str
    investments: List[InvestmentResponse]


class FundFamilySelect(BaseModel):
    name: str

class PurchaseFund(BaseModel):
    user_email: str
    scheme_code: str
    amount: float

class RegisterUser(BaseModel):
    email: EmailStr
    password: str