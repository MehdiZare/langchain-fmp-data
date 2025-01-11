"""FMPDataToolkit tools."""

import json
import logging
import os
import uuid
from enum import Enum
from typing import Optional, Type

from fmp_data import create_vector_store
from fmp_data.exceptions import AuthenticationError, ConfigError
from fmp_data.lc import EndpointVectorStore
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.errors import GraphRecursionError
from pydantic import BaseModel, Field

from langchain_fmp_data.agent import create_fmp_data_workflow

logger = logging.getLogger(__name__)


class ResponseFormat(str, Enum):
    """Output format for agent responses."""

    NATURAL_LANGUAGE = "natural_language"
    DATA_STRUCTURE = "data_structure"
    BOTH = "both"


class FMPDataToolInput(BaseModel):
    """Input schema for FMPData tool."""

    query: str = Field(
        ...,
        description="Natural language query about financial data",
        examples=[
            "What's the current price of AAPL?",
            "Show me TSLA's financial statements",
            "Get historical prices for GOOGL",
        ],
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.NATURAL_LANGUAGE,
        description=(
            "Format of the response (natural language, data structure, or both)" ""
        ),
    )


class FMPDataTool(BaseTool):
    """Tool for accessing financial data through the FMP API.

    Provides natural language interface to query financial data including:
    - Real-time market data
    - Stock prices and indexes
    - Financial statements
    - Company information
    - Economic indicators
    """

    name: str = "FMP Data"
    description: str = (
        "Use this tool for getting financial market data including stock prices, "
        "financial statements, company information, and economic indicators. "
        "Provides real-time and historical data access."
    )
    args_schema: Type[BaseModel] = FMPDataToolInput
    fmp_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    max_iterations: int = 30

    llm: Optional[ChatOpenAI] = None
    vector_store: Optional[EndpointVectorStore] = None
    thread_id: Optional[str] = None

    def __init__(
        self,
        fmp_api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        max_iterations: int = 30,
        temperature: float = 0,
    ) -> None:
        """Initialize FMP Data tool.

        Args:
            fmp_api_key: FMP API key (defaults to FMP_API_KEY env var)
            openai_api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            max_iterations: Maximum number of agent iterations
            temperature: Temperature for ChatOpenAI
            cache_dir: Directory for vector store cache
            store_name: Name for the vector store

        Raises:
            ValueError: If required API keys are missing
            RuntimeError: If vector store initialization fails
        """
        super().__init__()

        # Validate and set configuration
        self.fmp_api_key = fmp_api_key or os.getenv("FMP_API_KEY")
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")

        if not self.fmp_api_key or not self.openai_api_key:
            missing = []
            if not self.fmp_api_key:
                missing.append("FMP_API_KEY")
            if not self.openai_api_key:
                missing.append("OPENAI_API_KEY")
            raise ValueError(
                f"Missing required API keys: {', '.join(missing)}. "
                "Set as environment variables or pass to constructor."
            )

        self.max_iterations = max_iterations
        self.llm = ChatOpenAI(
            temperature=temperature, openai_api_key=self.openai_api_key
        )

        # Initialize vector store
        try:
            self.vector_store = create_vector_store(
                fmp_api_key=self.fmp_api_key,
                openai_api_key=self.openai_api_key,
            )
            if not self.vector_store:
                raise RuntimeError("Vector store initialization failed")
        except (ConfigError, AuthenticationError) as e:
            raise ValueError(f"Failed to initialize vector store: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error initializing vector store: {str(e)}")

    def _run(
        self,
        query: str,
        refresh_answer: bool = False,
        response_format: ResponseFormat = ResponseFormat.NATURAL_LANGUAGE,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str | dict:
        """Execute the tool with better error handling and response formatting."""
        try:
            thread_id = self.get_thread_id(refresh_answer)
            workflow = create_fmp_data_workflow(self.vector_store, self.llm)
            agent = workflow.compile(checkpointer=MemorySaver())

            messages = [
                SystemMessage(
                    content=(
                        "You are working as an expert financial analyst, helping an "
                        "AI assistant with financial related data gathering "
                        "and analysis. "
                        "Provide concise, accurate answers using the available tools. "
                        "Focus on delivering precise information without asking "
                        "follow-up questions."
                    )
                ),
                HumanMessage(content=query),
            ]

            config = {
                "configurable": {
                    "recursion_limit": self.max_iterations,
                    "thread_id": thread_id,
                }
            }

            final_state = agent.invoke({"messages": messages}, config=config)
            response = final_state.get("messages", [])[-1].content

            return self.format_response(response, response_format)

        except GraphRecursionError:
            error_msg = f"Analysis exceeded {self.max_iterations} iterations"
            logger.error(error_msg)
            return (
                {"error": error_msg}
                if response_format != ResponseFormat.NATURAL_LANGUAGE
                else error_msg
            )
        except Exception as e:
            error_msg = f"Error processing query: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return (
                {"error": error_msg}
                if response_format != ResponseFormat.NATURAL_LANGUAGE
                else error_msg
            )

    def validate_api_keys(self) -> None:
        """Validate required API keys are present."""
        missing = []
        if not self.fmp_api_key:
            missing.append("FMP_API_KEY")
        if not self.openai_api_key:
            missing.append("OPENAI_API_KEY")
        if missing:
            raise ValueError(
                f"Missing required API keys: {', '.join(missing)}. "
                "Set as environment variables or pass to constructor."
            )

    def initialize_vector_store(self) -> None:
        """Initialize or load vector store."""
        try:
            self.vector_store = create_vector_store(
                fmp_api_key=self.fmp_api_key,
                openai_api_key=self.openai_api_key,
            )
            if not self.vector_store:
                raise RuntimeError("Vector store initialization failed")
        except (ConfigError, AuthenticationError) as e:
            raise ValueError(f"Failed to initialize vector store: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error initializing vector store: {str(e)}")

    def get_thread_id(self, refresh: bool = False) -> str:
        """Get or create thread ID for conversation tracking."""
        if refresh or not self.thread_id:
            self.thread_id = str(uuid.uuid4())
        return self.thread_id

    @staticmethod
    def format_response(content: str, response_format: ResponseFormat) -> str | dict:
        """Format response based on specified format."""
        try:
            if response_format == ResponseFormat.DATA_STRUCTURE:
                # Attempt to parse response as JSON if it's structured data
                return json.loads(content)
            elif response_format == ResponseFormat.BOTH:
                return {
                    "natural_language": content,
                    "data": json.loads(content) if "{" in content else None,
                }
            return content
        except json.JSONDecodeError:
            if response_format != ResponseFormat.NATURAL_LANGUAGE:
                logger.warning(
                    "Failed to parse response as JSON, returning raw content"
                )
            return content
