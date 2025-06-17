from unittest.mock import patch

import pytest


import pytest
from unittest.mock import patch


@pytest.mark.asyncio
@pytest.mark.parametrize("response_data,expected_error_substrings", [
    ({"data": {"wrong_key": "value"}}, ["Error parsing API response:", "'amount'"]),
    ({"wrong_structure": {}}, ["Error parsing API response:", "'data'"]),
    ({"data": {"base": "BTC", "currency": "USD", "amount": "not_a_number"}},
     ["Error parsing API response:", "could not convert string to float"])
], ids=["missing_keys", "wrong_structure", "invalid_value"])
async def test_get_bitcoin_price_parsing_errors(load_api_endpoint, mock_aiohttp_client_session, response_data,
                                                expected_error_substrings):
    """Test API response parsing error handling with consolidated assertions."""
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
        error_msg = mock_logger.call_args[0][0]

        # Check that all expected substrings are in the error message
        for substring in expected_error_substrings:
            assert substring in error_msg


# Alternative approach - test for error patterns instead of exact messages
@pytest.mark.asyncio
@pytest.mark.parametrize("response_data,error_type", [
    ({"data": {"wrong_key": "value"}}, "parsing"),
    ({"wrong_structure": {}}, "parsing"),
    ({"data": {"base": "BTC", "currency": "USD", "amount": "not_a_number"}}, "parsing")
], ids=["missing_keys", "wrong_structure", "invalid_value"])
async def test_get_bitcoin_price_parsing_errors_flexible(load_api_endpoint, mock_aiohttp_client_session,
                                                         response_data, error_type):
    """Test API response parsing error handling with flexible error checking."""
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

        # Check that the log message indicates a parsing error
        actual_error_message = mock_logger.call_args[0][0]
        assert "Error parsing API response:" in actual_error_message

class TestAPIHandlerParsingErrors:
    """Dedicated class for testing API parsing errors with specific assertions."""

    @pytest.mark.asyncio
    async def test_missing_amount_key(self, load_api_endpoint, mock_aiohttp_client_session):
        """Test handling when 'amount' key is missing from response."""
        api_handler = load_api_endpoint
        _, mock_response = mock_aiohttp_client_session
        mock_response.json.return_value = {"data": {"wrong_key": "value"}}

        with patch.object(api_handler.logger, 'error') as mock_logger:
            price = await api_handler.get_bitcoin_price()

            assert price is None
            mock_logger.assert_called_once()
            error_msg = mock_logger.call_args[0][0]
            assert "Error parsing API response:" in error_msg
            assert "'amount'" in error_msg

    @pytest.mark.asyncio
    async def test_missing_data_key(self, load_api_endpoint, mock_aiohttp_client_session):
        """Test handling when 'data' key is missing from response."""
        api_handler = load_api_endpoint
        _, mock_response = mock_aiohttp_client_session
        mock_response.json.return_value = {"wrong_structure": {}}

        with patch.object(api_handler.logger, 'error') as mock_logger:
            price = await api_handler.get_bitcoin_price()

            assert price is None
            mock_logger.assert_called_once()
            error_msg = mock_logger.call_args[0][0]
            assert "Error parsing API response:" in error_msg
            assert "'data'" in error_msg

    @pytest.mark.asyncio
    async def test_invalid_price_value(self, load_api_endpoint, mock_aiohttp_client_session):
        """Test handling when price value cannot be converted to float."""
        api_handler = load_api_endpoint
        _, mock_response = mock_aiohttp_client_session
        mock_response.json.return_value = {"data": {"base": "BTC", "currency": "USD", "amount": "not_a_number"}}

        with patch.object(api_handler.logger, 'error') as mock_logger:
            price = await api_handler.get_bitcoin_price()

            assert price is None
            mock_logger.assert_called_once()
            error_msg = mock_logger.call_args[0][0]
            assert "Error parsing API response:" in error_msg
            assert "could not convert string to float" in error_msg
