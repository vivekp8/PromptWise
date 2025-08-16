from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class ThemeHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        theme = request.headers.get("X-DARK-MODE", "false")
        response = await call_next(request)
        response.headers["X-Favicon-Mode"] = "dark" if theme == "true" else "light"
        return response