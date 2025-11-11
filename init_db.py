import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent))

from app.core.database import init_db, close_db, init_redis, close_redis, AsyncSessionLocal
from app.core.security import get_password_hash
from app.core.logger import setup_logging, get_logger
from app.models.user import User

logger = get_logger(__name__)

async def create_test_user():
    """创建测试用户"""
    async with AsyncSessionLocal() as session:
        try:
            # 检查是否已存在测试用户
            from sqlalchemy import select
            result = await session.execute(select(User).where(User.username == "admin"))
            existing_user = result.scalar_one_or_none()
            
            if not existing_user:
                # 创建管理员用户
                admin_user = User(
                    username="admin",
                    email="admin@example.com",
                    password_hash=get_password_hash("admin123"),
                    full_name="Administrator",
                    is_active=True,
                    is_superuser=True
                )
                
                # 创建普通用户
                normal_user = User(
                    username="user",
                    email="user@example.com",
                    password_hash=get_password_hash("user123"),
                    full_name="Test User",
                    is_active=True,
                    is_superuser=False
                )
                
                session.add_all([admin_user, normal_user])
                await session.commit()
                
                logger.info("Test users created successfully:")
                logger.info("  - Admin: username=admin, password=admin123")
                logger.info("  - Normal: username=user, password=user123")
            else:
                logger.info("Test users already exist")
                
        except Exception as e:
            logger.error(f"Failed to create test users: {str(e)}")
            await session.rollback()
            raise
        finally:
            await session.close()

async def main():
    """主函数"""
    try:
        # 设置日志
        setup_logging()
        logger.info("Starting initialization...")
        
        # 初始化数据库
        await init_db()
        logger.info("Database initialized")
        
        # 初始化Redis
        await init_redis()
        logger.info("Redis initialized")
        
        # 创建测试用户
        await create_test_user()
        
        logger.info("Initialization completed successfully!")
        
    except Exception as e:
        logger.error(f"Initialization failed: {str(e)}")
        raise
    finally:
        # 关闭连接
        await close_db()
        await close_redis()

if __name__ == "__main__":
    asyncio.run(main())