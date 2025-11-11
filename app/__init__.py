"""SaltedFishOps Application Package"""

__version__ = "1.0.0"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.middleware import setup_middleware
from app.api.v1 import auth
from app.core.logger import setup_logging
from app.core.database import init_db, init_redis
import asyncio

# 初始化日志
setup_logging()

# 创建FastAPI实例
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 设置中间件（日志、链路等）
setup_middleware(app)

# 注册路由
app.include_router(auth.router, prefix="/api", tags=["authentication"])

@app.get("/")
async def root():
    return {"message": "Welcome to SaltedFishOps API"}

@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    # 初始化数据库和Redis
    await asyncio.gather(
        init_db(),
        init_redis()
    )

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    from app.core.database import close_db, close_redis
    await asyncio.gather(
        close_db(),
        close_redis()
    )