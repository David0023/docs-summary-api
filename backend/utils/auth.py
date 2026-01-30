import jwt
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel, ValidationError
from fastapi import HTTPException, status, Depends
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from utils.database import get_db
from core.config import settings
from models.user import User

# Where to get token from
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

class TokenData(BaseModel):
    sub: str
    exp: int
    iat: int
    role: str

def create_access_token(
    username: str,
    role: str
) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    iat = datetime.now(timezone.utc)
    to_encode = {
        "sub": username,
        "role": role,
        "exp": int(exp.timestamp()),
        "iat": int(iat.timestamp())
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return TokenData(**payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except jwt.PyJWTError:
            raise credentials_exception
    except ValidationError:
        raise credentials_exception
    
def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    token_data = decode_token(token)
    user = db.query(User).filter(User.username == token_data.sub).first()
    if user is None:
        raise credentials_exception
    return user

# Password
# Define password hashing scheme
password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)
