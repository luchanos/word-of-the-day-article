__all__ = ("technical_router",)
from fastapi import APIRouter, Depends

from api.ping.service import PingApp

technical_router = APIRouter(tags=["ping"])


@technical_router.get(path="/ping", responses={200: {"content": {"application/json": {"example": {"success": True}}}}})
def ping(ping_app: PingApp = Depends(PingApp)):
    """Check that service is alive."""
    return ping_app()
