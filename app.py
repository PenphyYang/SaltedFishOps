import uvicorn
from app.core.config import settings

if __name__ == "__main__":
    # 从app模块导入应用实例
    # 应用的初始化工作已经在app/__init__.py中完成
    uvicorn.run(
        "app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD
    )