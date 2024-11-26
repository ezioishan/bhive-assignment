import random

import requests

# Replace with your RapidAPI key
RAPIDAPI_KEY = "4a7bda4ea5msh9097f3211e751fap10a0ddjsnd91fa9544c29"
RAPIDAPI_URL = "https://latest-mutual-fund-nav.p.rapidapi.com/latest"

HEADERS = {
    "X-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "latest-mutual-fund-nav.p.rapidapi.com",
    "Content-Type": "application/json",
}

def fetch_fund_families():
    """Fetch all mutual fund families from the API."""
    response = requests.get(RAPIDAPI_URL, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"Error fetching data: {response.status_code}")
    data = response.json()
    fund_families = set(item["Mutual_Fund_Family"] for item in data)
    return set(fund_families)

def fetch_schemes(fund_family: str):
    """Fetch schemes for a given mutual fund family."""
    params = {"Mutual_Fund_Family": fund_family}
    response = requests.get(RAPIDAPI_URL, headers=HEADERS, params=params)
    if response.status_code != 200:
        raise Exception(f"Error fetching schemes: {response.status_code}")
    return response.json()

def purchase_fund(mutual_fund, portfolio):
    """Purchase mutual funds based on Scheme_Code and amount."""
    response = requests.get(
        RAPIDAPI_URL,
        headers=HEADERS,
        params={"Scheme_Code": mutual_fund.scheme_code}
    )
    print("purchase_fund")
    if response.status_code != 200:
        return None

    scheme_details = response.json()[0]
    nav = scheme_details["Net_Asset_Value"]
    quantity = mutual_fund.amount / nav

    portfolio[mutual_fund.user_email].append({
        "scheme_name": scheme_details["Scheme_Name"],
        "scheme_code": mutual_fund.scheme_code,
        "amount_invested": mutual_fund.amount,
        "quantity": round(quantity, 4),
        "current_nav": nav
    })

    return True