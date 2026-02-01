"""Extended unit tests for FMPDataTool"""

from unittest.mock import MagicMock, patch

import pytest
from langgraph.errors import GraphRecursionError

from langchain_fmp_data.tools import FMPDataTool, ResponseFormat


class TestFMPDataToolExtended:
    """Extended test suite for FMPDataTool"""

    @pytest.fixture(autouse=True)
    def setup_env(self, monkeypatch):
        """Setup test environment"""
        monkeypatch.setenv("FMP_API_KEY", "test_fmp_key")
        monkeypatch.setenv("OPENAI_API_KEY", "test_openai_key")

    def test_init_missing_fmp_key(self, monkeypatch):
        """Test initialization fails without FMP API key"""
        monkeypatch.delenv("FMP_API_KEY", raising=False)

        with pytest.raises(ValueError, match="FMP_API_KEY"):
            FMPDataTool()

    def test_init_missing_openai_key(self, monkeypatch):
        """Test initialization fails without OpenAI API key"""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            FMPDataTool()

    def test_init_vector_store_config_error(self):
        """Test initialization handles vector store config errors"""
        with patch("langchain_fmp_data.tools.create_vector_store") as mock_create_vs:
            from fmp_data.exceptions import ConfigError

            mock_create_vs.side_effect = ConfigError("Config error")

            with pytest.raises(ValueError, match="Failed to initialize vector store"):
                FMPDataTool()

    def test_init_vector_store_auth_error(self):
        """Test initialization handles authentication errors"""
        with patch("langchain_fmp_data.tools.create_vector_store") as mock_create_vs:
            from fmp_data.exceptions import AuthenticationError

            mock_create_vs.side_effect = AuthenticationError("Auth error")

            with pytest.raises(ValueError, match="Failed to initialize vector store"):
                FMPDataTool()

    def test_init_vector_store_unexpected_error(self):
        """Test initialization handles unexpected errors"""
        with patch("langchain_fmp_data.tools.create_vector_store") as mock_create_vs:
            mock_create_vs.side_effect = Exception("Unexpected")

            with pytest.raises(RuntimeError, match="Unexpected error"):
                FMPDataTool()

    def test_init_vector_store_returns_none(self):
        """Test initialization fails when vector store returns None"""
        with patch("langchain_fmp_data.tools.create_vector_store") as mock_create_vs:
            mock_create_vs.return_value = None

            with pytest.raises(RuntimeError, match="Vector store initialization failed"):
                FMPDataTool()

    @patch("langchain_fmp_data.tools.create_vector_store")
    @patch("langchain_fmp_data.tools.ChatOpenAI")
    def test_run_with_recursion_error(self, mock_chat, mock_create_vs):
        """Test _run handles recursion errors"""
        mock_vs = MagicMock()
        mock_create_vs.return_value = mock_vs

        tool = FMPDataTool()

        with patch("langchain_fmp_data.tools.create_fmp_data_workflow") as mock_workflow:
            mock_agent = MagicMock()
            mock_agent.invoke.side_effect = GraphRecursionError("Too many iterations")
            mock_workflow.return_value.compile.return_value = mock_agent

            result = tool.invoke({"query": "test query"})

            assert "exceeded" in result
            assert "30 iterations" in result

    @patch("langchain_fmp_data.tools.create_vector_store")
    @patch("langchain_fmp_data.tools.ChatOpenAI")
    def test_run_with_exception(self, mock_chat, mock_create_vs):
        """Test _run handles general exceptions"""
        mock_vs = MagicMock()
        mock_create_vs.return_value = mock_vs

        tool = FMPDataTool()

        with patch("langchain_fmp_data.tools.create_fmp_data_workflow") as mock_workflow:
            mock_workflow.side_effect = Exception("Something went wrong")

            result = tool.invoke({"query": "test query"})

            assert "Error processing query" in result
            assert "Something went wrong" in result

    @patch("langchain_fmp_data.tools.create_vector_store")
    @patch("langchain_fmp_data.tools.ChatOpenAI")
    def test_format_response_data_structure(self, mock_chat, mock_create_vs):
        """Test format_response with DATA_STRUCTURE format"""
        mock_vs = MagicMock()
        mock_create_vs.return_value = mock_vs

        tool = FMPDataTool()

        # Valid JSON
        json_content = '{"key": "value"}'
        result = tool.format_response(json_content, ResponseFormat.DATA_STRUCTURE)
        assert result == {"key": "value"}

        # Invalid JSON
        invalid_content = "not json"
        result = tool.format_response(invalid_content, ResponseFormat.DATA_STRUCTURE)
        assert result == "not json"

    @patch("langchain_fmp_data.tools.create_vector_store")
    @patch("langchain_fmp_data.tools.ChatOpenAI")
    def test_format_response_both(self, mock_chat, mock_create_vs):
        """Test format_response with BOTH format"""
        mock_vs = MagicMock()
        mock_create_vs.return_value = mock_vs

        tool = FMPDataTool()

        # With valid JSON
        json_content = '{"key": "value"}'
        result = tool.format_response(json_content, ResponseFormat.BOTH)
        assert isinstance(result, dict)
        assert "natural_language" in result
        assert "data" in result
        assert result["natural_language"] == json_content
        assert result["data"] == {"key": "value"}

        # Without valid JSON (text with curly brace)
        text_content = "Just text"
        result = tool.format_response(text_content, ResponseFormat.BOTH)
        assert isinstance(result, dict)
        assert result["natural_language"] == text_content
        assert result["data"] is None

    @patch("langchain_fmp_data.tools.create_vector_store")
    @patch("langchain_fmp_data.tools.ChatOpenAI")
    def test_format_response_natural_language(self, mock_chat, mock_create_vs):
        """Test format_response with NATURAL_LANGUAGE format"""
        mock_vs = MagicMock()
        mock_create_vs.return_value = mock_vs

        tool = FMPDataTool()

        content = "Natural language response"
        result = tool.format_response(content, ResponseFormat.NATURAL_LANGUAGE)
        assert result == content

    @patch("langchain_fmp_data.tools.create_vector_store")
    @patch("langchain_fmp_data.tools.ChatOpenAI")
    def test_get_thread_id(self, mock_chat, mock_create_vs):
        """Test get_thread_id method"""
        mock_vs = MagicMock()
        mock_create_vs.return_value = mock_vs

        tool = FMPDataTool()

        # First call creates new ID
        thread_id1 = tool.get_thread_id()
        assert thread_id1 is not None

        # Second call returns same ID
        thread_id2 = tool.get_thread_id()
        assert thread_id2 == thread_id1

        # Refresh creates new ID
        thread_id3 = tool.get_thread_id(refresh=True)
        assert thread_id3 != thread_id1
