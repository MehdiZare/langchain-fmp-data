import json
import logging
from typing import Annotated, Any, Dict, List, Literal, TypedDict, cast

from fmp_data.exceptions import FMPError
from fmp_data.lc import EndpointVectorStore
from langchain_core.messages import BaseMessage, ToolMessage
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.graph.message import add_messages

logger = logging.getLogger(__name__)


class State(TypedDict):
    """Type definition for the graph state."""

    messages: Annotated[List[BaseMessage], add_messages]


class ToolExecutionError(Exception):
    """Raised when there's an error executing a tool."""

    pass


class BasicToolNode:
    """
    A node that executes tools requested in the last AI message.

    Attributes:
        tools_by_name: Dictionary mapping tool names to tool instances

    Methods:
        __call__: Execute tools based on the input state
    """

    def __init__(self, tools: List[BaseTool]) -> None:
        """
        Initialize the tool node.

        Args:
            tools: List of available tools
        """
        self.tools_by_name: Dict[str, BaseTool] = {tool.name: tool for tool in tools}

    def __call__(self, state: Dict[str, Any]) -> Dict[str, List[ToolMessage]]:
        """
        Execute tools based on the input state.

        Args:
            state: Current state containing messages

        Returns:
            Dictionary containing tool execution results

        Raises:
            ValueError: If no message is found or invalid tool call
            ToolExecutionError: If tool execution fails
        """
        try:
            messages = state.get("messages", [])
            if not messages:
                raise ValueError("No messages found in input state")

            message = messages[-1]
            if not hasattr(message, "tool_calls"):
                raise ValueError("Last message contains no tool calls")

            outputs: List[ToolMessage] = []

            for tool_call in message.tool_calls:
                tool_name = tool_call["name"]
                if tool_name not in self.tools_by_name:
                    raise ValueError(f"Unknown tool: {tool_name}")

                try:
                    tool_result = self.tools_by_name[tool_name].invoke(
                        tool_call["args"]
                    )
                    outputs.append(
                        ToolMessage(
                            content=json.dumps(tool_result),
                            name=tool_name,
                            tool_call_id=tool_call["id"],
                        )
                    )
                except Exception as e:
                    logger.error(f"Tool execution failed: {str(e)}", exc_info=True)
                    raise ToolExecutionError(f"Failed to execute {tool_name}: {str(e)}")

            return {"messages": outputs}

        except (ValueError, ToolExecutionError) as e:
            logger.error(str(e))
            raise
        except Exception as e:
            logger.error(f"Unexpected error in tool execution: {str(e)}", exc_info=True)
            raise ToolExecutionError(f"Unexpected error: {str(e)}")


def should_continue(state: MessagesState) -> Literal["tools", "__end__"]:
    """
    Determine if the workflow should continue or end.

    Args:
        state: Current message state

    Returns:
        "tools" if more tool calls are needed, "__end__" otherwise
    """
    try:
        if not isinstance(state, dict) or "messages" not in state:
            logger.error("Invalid state format")
            return END

        messages = state["messages"]
        if not messages:
            logger.error("No messages in state")
            return END

        last_message = messages[-1]
        if not hasattr(last_message, "tool_calls"):
            logger.warning("Last message has no tool_calls attribute")
            return END

        return cast(
            Literal["tools", "__end__"],
            "tools" if last_message.tool_calls else "__end__",
        )

    except Exception as e:
        logger.error(f"Error in continuation check: {str(e)}", exc_info=True)
        return END


def validate_workflow_params(
    vector_store: EndpointVectorStore, model: ChatOpenAI, max_toolset_size: int
) -> None:
    """Validate workflow parameters."""
    if not isinstance(vector_store, EndpointVectorStore):
        raise TypeError("vector_store must be an EndpointVectorStore instance")

    if not isinstance(model, ChatOpenAI):
        raise TypeError("model must be a ChatOpenAI instance")

    if not isinstance(max_toolset_size, int):
        raise TypeError("max_toolset_size must be an integer")

    if max_toolset_size < 1:
        raise ValueError("max_toolset_size must be greater than 0")
    return None


def create_fmp_data_workflow(
    vector_store: EndpointVectorStore,
    model: ChatOpenAI,
    max_toolset_size: int = 10,
    max_retries: int = 3,
) -> StateGraph:
    """
    Create a workflow for processing FMP data queries.

    Args:
        vector_store: Vector store for tool retrieval
        model: ChatOpenAI model instance
        max_toolset_size: Maximum number of tools to use
        max_retries: Maximum number of retries for model calls (default: 3)

    Returns:
        Configured StateGraph instance

    Raises:
        FMPError: If there's an error with FMP data access
        ValueError: If invalid parameters are provided
    """
    if max_toolset_size < 1:
        raise ValueError("max_toolset_size must be greater than 0")

    def call_model(state: MessagesState) -> Dict[str, List[BaseMessage]]:
        """Process messages with the model."""
        retry_count = 0

        while retry_count < max_retries:
            try:
                messages = state["messages"]
                query = messages[-1].content

                match_tools = vector_store.get_tools(
                    query, k=max_toolset_size, provider="openai"
                )

                if not match_tools:
                    logger.warning("No matching tools found for query")
                    return {"messages": [model.invoke(messages)]}

                model_with_tools = model.bind_tools(tools=match_tools)
                response = model_with_tools.invoke(messages)

                return {"messages": [response]}

            except TimeoutError:
                retry_count += 1
                if retry_count == max_retries:
                    raise
                logger.warning(
                    f"Model call timeout, attempt {retry_count}/{max_retries}"
                )
                continue
            except FMPError as e:
                logger.error(f"FMP data access error: {str(e)}")
                raise
            except Exception as e:
                logger.error(f"Error in model processing: {str(e)}", exc_info=True)
                raise

    try:
        # Initialize workflow components
        all_tools = vector_store.get_tools()
        tool_node = BasicToolNode(all_tools)
        workflow = StateGraph(MessagesState)

        # Add nodes and edges
        workflow.add_node("agent", call_model)
        workflow.add_node("tools", tool_node)
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges("agent", should_continue)
        workflow.add_edge("tools", "agent")

        return workflow

    except Exception as e:
        logger.error(f"Error creating workflow: {str(e)}", exc_info=True)
        raise


__all__ = ["create_fmp_data_workflow"]
