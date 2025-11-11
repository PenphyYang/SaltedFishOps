from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.core.config import settings
from app.core.logger import get_logger
from app.models.user import User
from app.schemas.user import Token, LoginRequest

router = APIRouter()
logger = get_logger(__name__)

@router.post("/login", response_model=Token, summary="用户登录")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    用户登录接口
    
    - **username**: 用户名
    - **password**: 密码
    
    返回JWT访问令牌
    """
    # 查询用户
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()
    
    # 验证用户和密码
    if not user or not verify_password(form_data.password, user.password_hash):
        logger.warning(f"Login failed for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 检查用户是否激活
    if not user.is_active:
        logger.warning(f"Inactive user tried to login: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    logger.info(f"User logged in successfully: {user.username}")
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@router.post("/login/json", response_model=Token, summary="用户登录(JSON格式)")
async def login_json(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    用户登录接口（JSON格式）
    
    - **username**: 用户名
    - **password**: 密码
    
    返回JWT访问令牌
    """
    # 查询用户
    result = await db.execute(select(User).where(User.username == login_data.username))
    user = result.scalar_one_or_none()
    
    # 验证用户和密码
    if not user or not verify_password(login_data.password, user.password_hash):
        logger.warning(f"Login failed for user: {login_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 检查用户是否激活
    if not user.is_active:
        logger.warning(f"Inactive user tried to login: {login_data.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    logger.info(f"User logged in successfully: {user.username}")
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }