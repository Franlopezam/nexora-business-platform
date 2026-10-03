from collections import defaultdict, deque
from time import monotonic

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from ..config import settings


class SimpleRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.requests = defaultdict(deque)

    async def dispatch(self, request, call_next):
        client = request.client.host if request.client else "unknown"
        now = monotonic()
        bucket = self.requests[client]

        while bucket and now - bucket[0] > 60:
            bucket.popleft()

        if len(bucket) >= settings.rate_limit:
            return JSONResponse({"detail": "Too many requests"}, status_code=429)

        bucket.append(now)
        return await call_next(request)
