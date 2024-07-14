import pytest
import asyncio
from unittest.mock import AsyncMock

from utils.retry import retry


@retry(n=3, delay=1)
async def always_failing_function():
    raise ValueError("This function always fails")


@retry(n=3, delay=1)
async def succeed_after_retries(mock: AsyncMock):
    if not mock.called:
        mock()
        raise ValueError("Failing first time")
    return "Success"


@retry(n=3, delay=1)
async def succeed_immediately():
    return "Success"


async def test_always_failing_function():
    with pytest.raises(ValueError, match="This function always fails"):
        await always_failing_function()


async def test_succeed_after_retries():
    mock = AsyncMock()
    result = await succeed_after_retries(mock)
    assert result == "Success"
    assert mock.call_count == 1


async def test_succeed_immediately():
    result = await succeed_immediately()
    assert result == "Success"


async def test_retry_delay(mocker):
    mock = AsyncMock()
    sleep_mock = mocker.patch("asyncio.sleep", side_effect=asyncio.sleep)

    with pytest.raises(ValueError, match="This function always fails"):
        await always_failing_function()

    assert sleep_mock.call_count == 2


async def test_retry_delay_succeed_after_retries(mocker):
    mock = AsyncMock()
    sleep_mock = mocker.patch("asyncio.sleep", side_effect=asyncio.sleep)
    result = await succeed_after_retries(mock)
    assert result == "Success"
    assert sleep_mock.call_count == 1
