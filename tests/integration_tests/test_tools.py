from typing import Type
from unittest import mock

import pytest
from langchain_tests.integration_tests import ToolsIntegrationTests

from langchain_fmp_data.tools import FMPDataTool, ResponseFormat


class TestFMPDataToolIntegration(ToolsIntegrationTests):
    """Integration tests for FMPDataTool with LangChain"""

    @pytest.fixture(autouse=True)
    def setup_mocks(self, monkeypatch):
        """Setup test environment and mocks"""
        # Mock environment variables
        monkeypatch.setenv("FMP_API_KEY", "test_key")
        monkeypatch.setenv("OPENAI_API_KEY", "test_key")

        # Mock dependencies
        workflow_mock = mock.MagicMock()
        workflow_mock.compile.return_value.invoke.return_value = {
            "messages": [mock.MagicMock(content='{"symbol": "AAPL", "price": 150}')]
        }

        monkeypatch.setattr(
            "langchain_fmp_data.tools.create_vector_store",
            mock.MagicMock(return_value=mock.MagicMock()),
        )
        monkeypatch.setattr(
            "langchain_fmp_data.tools.ChatOpenAI",
            mock.MagicMock(return_value=mock.MagicMock()),
        )
        monkeypatch.setattr(
            "langchain_fmp_data.tools.create_fmp_data_workflow",
            mock.MagicMock(return_value=workflow_mock),
        )

    @property
    def tool_constructor(self) -> Type[FMPDataTool]:
        """Get the tool constructor"""
        return FMPDataTool

    @property
    def tool_constructor_params(self) -> dict:
        """Get parameters for tool construction"""
        return {
            "max_iterations": 3,
            "temperature": 0.0,
        }

    @property
    def tool_invoke_params_example(self) -> dict:
        """Get example parameters for tool invocation"""
        return {
            "query": "What is the current price of AAPL?",
            "response_format": ResponseFormat.NATURAL_LANGUAGE,
        }
