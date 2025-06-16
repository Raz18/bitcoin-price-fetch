from api_handler import APIHandler
import pytest
from unittest.mock import MagicMock, patch, AsyncMock

@pytest.fixture(scope="session")
def mock_aiohttp_client_session():
    """Mock aiohttp ClientSession for API testing."""
    with patch('aiohttp.ClientSession') as mock_session:
        mock_response = AsyncMock()
        # MagicMock instead of AsyncMock for raise_for_status
        mock_response.raise_for_status = MagicMock()  # Changed from AsyncMock
        mock_response.json = AsyncMock(return_value={"data": {"base": "BTC", "currency": "USD", "amount": "105565.74"}})

        # object that supports async context management
        mock_response.__aenter__.return_value = mock_response
        mock_response.__aexit__.return_value = None

        # Create a session instance
        session_instance = MagicMock()
        session_instance.get.return_value = mock_response

        # Make session_instance support async context management
        session_instance.__aenter__.return_value = session_instance
        session_instance.__aexit__.return_value = None

        mock_session.return_value = session_instance

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
