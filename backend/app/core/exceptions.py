from fastapi import Request
from fastapi.responses import JSONResponse
import uuid

class GlobalAPIException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

async def global_exception_handler(request: Request, exc: GlobalAPIException):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "request_id": request_id}
    )
