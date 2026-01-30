from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.security import decode_token, credentials_exception
from utils.database import get_db
from models.user import User

# Where to get token from
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    token_data = decode_token(token)
    user = db.query(User).filter(User.username == token_data.sub).first()
    if user is None:
        raise credentials_exception
    return user