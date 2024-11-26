from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from auth import authenticate_user, create_access_token, get_current_user, register_user
from schemas import FundFamilySelect, PurchaseFund, RegisterUser
from utils import fetch_fund_families, fetch_schemes, purchase_fund

app = FastAPI()

# In-memory storage
users = {}
portfolio = {}

@app.post("/register")
def register(user: RegisterUser):
    """Register a new user."""
    return register_user(user.email, user.password)

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Endpoint to log in and retrieve an access token."""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user})
    return {"access_token": access_token, "token_type": "bearer"}


'''Returns a distinct list of mutual fund families'''
@app.get("/fund-family")
def get_fund_families(current_user: str = Depends(get_current_user)):
    """Fetch all mutual fund families (protected route)."""
    fund_families = fetch_fund_families()
    return {"fund_families": fund_families}

'''
Returns a list of schemes specific to the fund family mentioned
NOTE: Request body required
Example:
{
    "name" : "JM Financial Mutual Fund"
}
'''
@app.get("/fund-family/schemes")
def get_schemes(fund_family: FundFamilySelect, current_user: str = Depends(get_current_user)):
    """Fetch schemes for a selected mutual fund family (protected route)."""
    schemes = fetch_schemes(fund_family.name)
    if not schemes:
        raise HTTPException(status_code=404, detail="No schemes found for the given fund family")
    return {"fund_family": fund_family.name, "schemes": schemes}

@app.post("/funds/purchase")
def purchase(mutual_fund: PurchaseFund, current_user: str = Depends(get_current_user)):
    """Purchase funds by specifying Scheme_Code and amount (protected route)."""
    if current_user not in portfolio:
        portfolio[current_user] = []

    result = purchase_fund(mutual_fund, portfolio)
    if not result:
        raise HTTPException(status_code=400, detail="Purchase failed")
    return {"message": "Purchase successful"}


@app.get("/portfolio")
def view_portfolio(current_user: str = Depends(get_current_user)):
    """View all funds purchased by the logged-in user (protected route)."""
    user_portfolio = portfolio.get(current_user, [])
    if not user_portfolio:
        return {"message": "No funds purchased yet"}
    return {"user_email": current_user, "portfolio": user_portfolio}
