from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from pydantic import BaseModel
from dotenv import load_dotenv

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

# Load local env variables
load_dotenv()

# Secret key for signing JWTs
SECRET_KEY = os.getenv('API_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Mock user database
users_db = {}

class TokenData(BaseModel):
    email: str = None

def verify_password(plain_password, hashed_password):
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def authenticate_user(email: str, password: str):
    """Authenticate user against the mock database."""
    user = users_db.get(email)
    if user and verify_password(password, user["password"]):
        return email
    return None

def create_access_token(data: dict):
    """Create a JWT token with expiration."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    """Decode the JWT and get the current user."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication")

def register_user(email: str, password: str):
    """Register a new user in the database."""
    if email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = hash_password(password)
    users_db[email] = {"password": hashed_password}
    return {"message": "User registered successfully"}
