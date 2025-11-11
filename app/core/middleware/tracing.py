import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.datastructures import Headers

from app.core.logger import get_logger, REQUEST_ID, TRACE_ID
from app.core.config import settings

logger = get_logger(__name__)

class TracingMiddleware(BaseHTTPMiddleware):
    """链路追踪中间件"""
    
    async def dispatch(self, request: Request, call_next):
        # 生成或获取请求ID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))
        
        # 设置上下文变量
        REQUEST_ID.set(request_id)
        TRACE_ID.set(trace_id)
        
        # 记录请求开始
        start_time = time.time()
        logger.info(f"Request: {request.method} {request.url.path}")
        
        try:
            # 调用下一个处理程序
            response = await call_next(request)
            
            # 添加追踪信息到响应头
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Trace-ID"] = trace_id
            
            # 计算处理时间
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            
            logger.info(f"Response: {response.status_code} - {process_time:.3f}s")
            
            return response
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}", exc_info=True)
            raise

class ExceptionMiddleware(BaseHTTPMiddleware):
    """异常处理中间件"""
    
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
            return Response(
                content=f"{settings.ENVIRONMENT == 'development' and str(e) or 'Internal Server Error'}",
                status_code=500,
                headers={"Content-Type": "text/plain"}
            )