from app.core.logger import get_logger
from app.core.config import settings

logger = get_logger(__name__)

def setup_middleware(app):
    """设置所有中间件"""
    # 添加链路追踪中间件
    from app.core.middleware.tracing import TracingMiddleware, ExceptionMiddleware
    app.add_middleware(TracingMiddleware)
    
    # 添加异常处理中间件
    app.add_middleware(ExceptionMiddleware)
    
    # 如果启用了追踪
    if settings.TRACING_ENABLED:
        # 这里可以添加OpenTelemetry等追踪工具的中间件
        pass
    
    logger.info("Middlewares setup completed")