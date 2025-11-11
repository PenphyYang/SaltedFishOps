from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """获取密码哈希值"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Optional[dict]:
    """解码JWT令牌"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError as e:
        logger.error(f"Failed to decode token: {str(e)}")
        return None

class PermissionChecker:
    """权限检查器"""
    
    @staticmethod
    def is_active(user) -> bool:
        """检查用户是否激活"""
        return user.is_active
    
    @staticmethod
    def is_superuser(user) -> bool:
        """检查用户是否为超级用户"""
        return user.is_superuser
    
    @staticmethod
    def has_permission(user, required_permission: str) -> bool:
        """检查用户是否有特定权限"""
        # 这里可以实现更复杂的权限检查逻辑
        # 例如基于角色的访问控制
        if user.is_superuser:
            return True
        # TODO: 实现具体的权限检查逻辑
        return False