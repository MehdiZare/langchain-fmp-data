from typing import Dict, Tuple, Type
from unittest import mock

import pytest
from langchain_tests.unit_tests import ToolsUnitTests

from langchain_fmp_data.tools import FMPDataTool, ResponseFormat


class TestFMPDataTool(ToolsUnitTests):
    """Unit tests for FMPDataTool"""

    @pytest.fixture(autouse=True)
    def setup_mocks(self, monkeypatch):
        """Setup test environment and mocks"""
        # Mock environment variables
        monkeypatch.setenv("FMP_API_KEY", "test_fmp_key")
        monkeypatch.setenv("OPENAI_API_KEY", "test_openai_key")

        # Mock external dependencies
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
        """Returns the tool constructor"""
        return FMPDataTool

    @property
    def tool_constructor_params(self) -> dict:
        """Returns parameters for tool initialization"""
        return {
            "max_iterations": 5,
            "temperature": 0.0,
        }

    @property
    def tool_invoke_params_example(self) -> dict:
        """Returns example parameters for tool invocation"""
        return {
            "query": "What is the current price of AAPL?",
            "response_format": ResponseFormat.NATURAL_LANGUAGE,
        }

    @property
    def init_from_env_params(self) -> Tuple[Dict, Dict, Dict]:
        """Return parameters for environment-based initialization"""
        env_vars = {
            "FMP_API_KEY": "test_fmp_key",
            "OPENAI_API_KEY": "test_openai_key",
        }
        init_params = {}
        expected_attrs = {
            "fmp_api_key": "test_fmp_key",
            "openai_api_key": "test_openai_key",
            "max_iterations": 30,  # default value
        }
        return env_vars, init_params, expected_attrs
