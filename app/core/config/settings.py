from typing import List, Optional, Any
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # 项目基本信息
    PROJECT_NAME: str = "SaltedFishOps"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "异步分布式运维系统API"
    
    # 运行环境
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    
    # CORS配置
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # 数据库配置 - PostgreSQL
    DATABASE_URL: str = "postgresql+asyncpg://admin:password@localhost:5432/example_db"
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_PASSWORD: Optional[str] = None
    
    # 认证配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # 链路追踪配置
    TRACING_ENABLED: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            """解析环境变量值"""
            if field_name == "BACKEND_CORS_ORIGINS":
                return raw_val.split(",")
            return raw_val

@lru_cache()
def get_settings():
    """获取配置单例"""
    return Settings()

settings = get_settings()