from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from email_validator import EmailNotValidError
from utils.validator import validate_email_address
from core.dependencies import get_db
from core.security import verify_password, create_access_token, hash_password
from schemas.user import UserCreateResponse, UserCreateRequest
from repositories.user_repository import get_one_user, create_user

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreateRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        validate_email_address(user_data.email)
    except EmailNotValidError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    if await get_one_user(db, username=user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    if await get_one_user(db, email=user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    new_user = await create_user(
        db, username=user_data.username, email=user_data.email, 
        hashed_password=hash_password(user_data.password)
    )
    return new_user
    

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    db: AsyncSession = Depends(get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = await get_one_user(db, username=form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username Not Found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "access_token": create_access_token(
            username=user.username,
            role="user"
        ),
        "token_type": "bearer"
    }