from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
import aioredis
from typing import AsyncGenerator

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

# SQLAlchemy配置
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=10,
    max_overflow=20
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

# Redis连接池
redis_pool = None

async def init_redis():
    """初始化Redis连接池"""
    global redis_pool
    try:
        redis_pool = await aioredis.from_url(
            settings.REDIS_URL,
            password=settings.REDIS_PASSWORD,
            encoding="utf-8",
            decode_responses=True
        )
        logger.info("Redis connected successfully")
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {str(e)}")
        raise

async def get_redis():
    """获取Redis连接"""
    global redis_pool
    if not redis_pool:
        await init_redis()
    return redis_pool

async def close_redis():
    """关闭Redis连接"""
    global redis_pool
    if redis_pool:
        await redis_pool.close()
        logger.info("Redis connection closed")

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """获取数据库会话"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_db():
    """初始化数据库（创建表）"""
    async with engine.begin() as conn:
        # 导入所有模型以确保它们被注册
        from app.models import user  # noqa
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized")

async def close_db():
    """关闭数据库连接"""
    await engine.dispose()
    logger.info("Database connection closed")