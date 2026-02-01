"""Unit tests for FMPDataToolkit"""

from unittest.mock import MagicMock, patch

import pytest

from langchain_fmp_data.toolkits import FMPDataToolkit


class TestFMPDataToolkit:
    """Test suite for FMPDataToolkit"""

    @pytest.fixture(autouse=True)
    def setup_env(self, monkeypatch):
        """Setup test environment"""
        monkeypatch.setenv("FMP_API_KEY", "test_fmp_key")
        monkeypatch.setenv("OPENAI_API_KEY", "test_openai_key")

    def test_init_with_api_keys(self):
        """Test initialization with explicit API keys"""
        with patch("fmp_data.lc.create_vector_store") as mock_create_vs:
            mock_vs = MagicMock()
            mock_vs.get_tools.return_value = [MagicMock(), MagicMock()]
            mock_create_vs.return_value = mock_vs

            toolkit = FMPDataToolkit(
                query="test query",
                num_results=5,
                fmp_api_key="explicit_fmp_key",
                openai_api_key="explicit_openai_key",
            )

            assert toolkit.fmp_api_key == "explicit_fmp_key"
            assert toolkit.openai_api_key == "explicit_openai_key"
            assert toolkit.query == "test query"
            assert toolkit.num_results == 5
            mock_create_vs.assert_called_once_with(
                fmp_api_key="explicit_fmp_key", openai_api_key="explicit_openai_key"
            )

    def test_init_from_env_vars(self):
        """Test initialization using environment variables"""
        with patch("fmp_data.lc.create_vector_store") as mock_create_vs:
            mock_vs = MagicMock()
            mock_vs.get_tools.return_value = [MagicMock()]
            mock_create_vs.return_value = mock_vs

            toolkit = FMPDataToolkit(query="test query", num_results=3)

            assert toolkit.fmp_api_key == "test_fmp_key"
            assert toolkit.openai_api_key == "test_openai_key"
            mock_create_vs.assert_called_once_with(
                fmp_api_key="test_fmp_key", openai_api_key="test_openai_key"
            )

    def test_init_missing_api_keys(self, monkeypatch):
        """Test initialization fails with missing API keys"""
        monkeypatch.delenv("FMP_API_KEY", raising=False)
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        with pytest.raises(ValueError, match="Missing required API keys"):
            FMPDataToolkit(query="test query")

    def test_init_missing_query(self):
        """Test initialization fails without query"""
        with pytest.raises(ValueError, match="query parameter is required"):
            FMPDataToolkit(query="")

    def test_get_tools(self):
        """Test get_tools method returns tools"""
        with patch("fmp_data.lc.create_vector_store") as mock_create_vs:
            mock_tools = [MagicMock(name="tool1"), MagicMock(name="tool2")]
            mock_vs = MagicMock()
            mock_vs.get_tools.return_value = mock_tools
            mock_create_vs.return_value = mock_vs

            toolkit = FMPDataToolkit(query="test query", num_results=2)
            tools = toolkit.get_tools()

            assert tools == mock_tools
            assert len(tools) == 2

    def test_import_error_handling(self):
        """Test proper error handling when fmp_data is not installed"""
        with patch.dict("sys.modules", {"fmp_data.lc": None}):
            with pytest.raises(ImportError, match="Could not import fmp_data"):
                FMPDataToolkit(query="test")

    def test_init_with_partial_api_keys(self, monkeypatch):
        """Test initialization with only one API key missing"""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            FMPDataToolkit(query="test query")

    def test_num_results_parameter(self):
        """Test different num_results values"""
        with patch("fmp_data.lc.create_vector_store") as mock_create_vs:
            mock_vs = MagicMock()
            mock_vs.get_tools.return_value = []
            mock_create_vs.return_value = mock_vs

            toolkit = FMPDataToolkit(query="test", num_results=10)
            toolkit.get_tools()

            mock_vs.get_tools.assert_called_once_with(query="test", k=10)
