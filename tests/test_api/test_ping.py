import httpx

from api.ping.service import PingApp


def test_ping_app():
    ping_app = PingApp()
    ping_result = ping_app()
    assert ping_result == {"success": True}


async def test_ping_api(test_cli: httpx.AsyncClient):
    response = await test_cli.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"success": True}
