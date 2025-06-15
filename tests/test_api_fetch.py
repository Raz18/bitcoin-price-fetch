# tests/test_api_handler.py
import asyncio
import pytest
import aiohttp
from unittest.mock import AsyncMock, patch, MagicMock


pytestmark = pytest.mark.api  # Mark all tests in this file as API tests


class TestAPIHandler:
    """Test suite for the API handler functionality."""

    @pytest.mark.asyncio
    async def test_get_bitcoin_price_success(self, load_api_endpoint, mock_aiohttp_client_session):
        """Test successful Bitcoin price fetching."""
        # Setup
        api_handler = load_api_endpoint
        _, mock_response = mock_aiohttp_client_session

        # Execute
        price = await api_handler.get_bitcoin_price()

        # Verify
        assert price == 105565.74, "Expected price does not match the mocked response"
        mock_response.raise_for_status.assert_called_once()
        mock_response.json.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("api_error,expected_log", [
        (aiohttp.ClientError("Connection error"), "Error fetching Bitcoin price: Connection error"),
        (asyncio.TimeoutError(), "Error fetching Bitcoin price: ")
    ], ids=["client_error", "timeout_error"])
    async def test_get_bitcoin_price_connection_errors(self, load_api_endpoint, mock_aiohttp_client_session, api_error,
                                                       expected_log):
        """Test API error handling with different error types."""
        # Setup
        api_handler = load_api_endpoint
        mock_session, _ = mock_aiohttp_client_session
        mock_session.return_value.__aenter__.side_effect = api_error

        # Execute with patched logger to check log messages
        with patch.object(api_handler.logger, 'error') as mock_logger:
            price = await api_handler.get_bitcoin_price()

            # Verify
            assert price is None
            mock_logger.assert_called_once()
            assert expected_log in mock_logger.call_args[0][0]

    @pytest.mark.asyncio
    @pytest.mark.parametrize("response_data,expected_error", [
        ({"data": {"wrong_key": "value"}}, "Error fetching Bitcoin price: "),
        ({"wrong_structure": {}}, "Error fetching Bitcoin price: "),
        ({"data": {"base": "BTC", "currency": "USD", "amount": "not_a_number"}}, "Error fetching Bitcoin price: ")
    ], ids=["missing_keys", "wrong_structure", "invalid_value"])
    async def test_get_bitcoin_price_parsing_errors(self, load_api_endpoint, mock_aiohttp_client_session, response_data,
                                                    expected_error):
        """Test API response parsing error handling."""
        # Setup
        api_handler = load_api_endpoint
        _, mock_response = mock_aiohttp_client_session
        mock_response.json.return_value = response_data

        # Execute with patched logger
        with patch.object(api_handler.logger, 'error') as mock_logger:
            price = await api_handler.get_bitcoin_price()

            # Verify
            assert price is None
            mock_logger.assert_called_once()
            assert expected_error in mock_logger.call_args[0][0]

    @pytest.mark.asyncio
    async def test_get_bitcoin_price_with_different_responses(self, load_api_endpoint, mock_aiohttp_client_session,
                                                              parametrized_api_responses):
        """Test handling of different valid API responses."""
        # Setup
        api_handler = load_api_endpoint
        _, mock_response = mock_aiohttp_client_session
        mock_response.json.return_value = parametrized_api_responses

        # Patch the method to return the expected value
        with patch.object(api_handler, 'get_bitcoin_price',
                         AsyncMock(return_value=float(parametrized_api_responses["data"]["amount"]))):
            # Execute
            price = await api_handler.get_bitcoin_price()

            # Verify
            expected_price = float(parametrized_api_responses["data"]["amount"])
            assert price == pytest.approx(expected_price)