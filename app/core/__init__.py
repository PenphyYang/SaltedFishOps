"""Core functionality package"""

# 导入配置模块
from app.core.config import settings, get_settings

# 导入数据库模块
from app.core.database import (
    AsyncSessionLocal,
    Base,
    get_db,
    init_db,
    close_db,
    init_redis,
    get_redis,
    close_redis
)

# 导入安全模块
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_token,
    PermissionChecker
)

# 导入日志模块
from app.core.logger import (
    setup_logging,
    get_logger,
    LogContext,
    REQUEST_ID,
    TRACE_ID
)

# 导入中间件模块
from app.core.middleware import (
    setup_middleware,
    TracingMiddleware,
    ExceptionMiddleware
)

# 导入依赖模块
from app.core.dependencies import (
    get_current_user,
    get_current_active_user,
    get_current_superuser,
    PermissionDependency,
    oauth2_scheme
)

__all__ = [
    # 配置
    "settings", "get_settings",
    # 数据库
    "AsyncSessionLocal", "Base", "get_db", "init_db", "close_db",
    "init_redis", "get_redis", "close_redis",
    # 安全
    "verify_password", "get_password_hash", "create_access_token",
    "decode_token", "PermissionChecker",
    # 日志
    "setup_logging", "get_logger", "LogContext", "REQUEST_ID", "TRACE_ID",
    # 中间件
    "setup_middleware", "TracingMiddleware", "ExceptionMiddleware",
    # 依赖
    "get_current_user", "get_current_active_user", "get_current_superuser",
    "PermissionDependency", "oauth2_scheme"
]