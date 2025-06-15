# tests/conftest.py
import os
import json
import pytest
import asyncio
from datetime import datetime
from unittest.mock import MagicMock, patch, AsyncMock

from api_handler import APIHandler


@pytest.fixture(scope="session")
def mock_aiohttp_client_session():
    """Mock aiohttp ClientSession for API testing."""
    with patch('aiohttp.ClientSession') as mock_session:
        mock_response = AsyncMock()
        mock_response.raise_for_status = AsyncMock()
        mock_response.json = AsyncMock()

        # Create a session instance
        session_instance = AsyncMock()

        # Create an object that can be used with async with
        get_result = MagicMock()  # Using MagicMock instead of AsyncMock
        get_result.__aenter__ = AsyncMock(return_value=mock_response)
        get_result.__aexit__ = AsyncMock(return_value=None)

        # Make session.get return this object directly
        session_instance.get = MagicMock(return_value=get_result)  # Not async

        mock_session.return_value.__aenter__.return_value = session_instance

        yield mock_session, mock_response

@pytest.fixture(scope="session")
def load_api_endpoint(mock_aiohttp_client_session):
    """Fixture to provide a pre-configured API handler with mocked responses."""
    _, mock_response = mock_aiohttp_client_session
    mock_response.json.return_value = {"data": {"base": "BTC", "currency": "USD", "amount": "105565.74"}}

    api_handler = APIHandler("https://api.coinbase.com/v2/prices/BTC-USD/spot")
    return api_handler

@pytest.fixture
def parametrized_api_responses(request):
    """Provide different valid mock API responses for testing."""
    responses = {
        "standard": {"data": {"base": "BTC", "currency": "USD", "amount": "105565.74"}},
        "lower_price": {"data": {"base": "BTC", "currency": "USD", "amount": "95000.00"}},
        "higher_price": {"data": {"base": "BTC", "currency": "USD", "amount": "110000.00"}},
        "integer_price": {"data": {"base": "BTC", "currency": "USD", "amount": "100000"}},
    }

    # Default to standard response if no param is provided
    param = getattr(request, "param", "standard")
    return responses.get(param, responses["standard"])
