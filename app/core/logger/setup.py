import logging
import uuid
import time
from typing import Optional
from contextvars import ContextVar

from app.core.config import settings

# 上下文变量用于链路追踪
REQUEST_ID: ContextVar[Optional[str]] = ContextVar("request_id", default=None)
TRACE_ID: ContextVar[Optional[str]] = ContextVar("trace_id", default=None)

class CustomFormatter(logging.Formatter):
    """自定义日志格式器"""
    
    def format(self, record):
        # 添加链路追踪信息
        record.request_id = REQUEST_ID.get() or "-"
        record.trace_id = TRACE_ID.get() or "-"
        record.process_time = getattr(record, "process_time", "-")
        
        # 自定义日志格式
        if settings.ENVIRONMENT == "development":
            self._style._fmt = "%(asctime)s - %(name)s - %(levelname)s - [%(request_id)s] - [%(trace_id)s] - %(message)s"
        else:
            self._style._fmt = '{"timestamp":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","request_id":"%(request_id)s","trace_id":"%(trace_id)s","message":"%(message)s"}'
        
        return super().format(record)

def setup_logging():
    """配置日志系统"""
    # 获取根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # 清除现有的处理器
    root_logger.handlers.clear()
    
    # 添加控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(CustomFormatter())
    root_logger.addHandler(console_handler)
    
    # 在生产环境中添加文件处理器
    if settings.ENVIRONMENT == "production":
        file_handler = logging.FileHandler("app.log")
        file_handler.setFormatter(CustomFormatter())
        root_logger.addHandler(file_handler)

def get_logger(name: str = "app") -> logging.Logger:
    """获取日志记录器"""
    return logging.getLogger(name)

class LogContext:
    """日志上下文管理器，用于记录请求处理时间"""
    
    def __init__(self, logger: logging.Logger, message: str):
        self.logger = logger
        self.message = message
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        self.logger.info(f"{self.message} - started")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        process_time = time.time() - self.start_time
        extra = {"process_time": f"{process_time:.3f}s"}
        if exc_type:
            self.logger.error(f"{self.message} - failed", exc_info=True, extra=extra)
        else:
            self.logger.info(f"{self.message} - completed", extra=extra)