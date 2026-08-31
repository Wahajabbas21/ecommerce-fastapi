from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class NotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message

def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(request: Request, exc: NotFoundException):
        return JSONResponse(
            status_code=404,
            content={"detail": exc.message}
        )
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"detail": "An unexpected error occurred. Please try again later."}
        )