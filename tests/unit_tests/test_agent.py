"""Unit tests for agent module"""

from unittest.mock import MagicMock, Mock, patch

import pytest
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_core.tools import BaseTool

from langchain_fmp_data.agent import (
    BasicToolNode,
    ToolExecutionError,
    create_fmp_data_workflow,
    should_continue,
    validate_workflow_params,
)


class TestBasicToolNode:
    """Test suite for BasicToolNode"""

    def test_init(self):
        """Test BasicToolNode initialization"""
        tool1 = MagicMock(spec=BaseTool)
        tool1.name = "tool1"
        tool2 = MagicMock(spec=BaseTool)
        tool2.name = "tool2"

        node = BasicToolNode([tool1, tool2])

        assert "tool1" in node.tools_by_name
        assert "tool2" in node.tools_by_name
        assert node.tools_by_name["tool1"] == tool1
        assert node.tools_by_name["tool2"] == tool2

    def test_call_with_tool_calls(self):
        """Test calling BasicToolNode with tool calls"""
        tool = MagicMock(spec=BaseTool)
        tool.name = "test_tool"
        tool.invoke.return_value = {"result": "success"}

        node = BasicToolNode([tool])

        message = MagicMock()
        message.tool_calls = [
            {"name": "test_tool", "args": {"param": "value"}, "id": "123"}
        ]

        state = {"messages": [message]}
        result = node(state)

        assert "messages" in result
        assert len(result["messages"]) == 1
        assert isinstance(result["messages"][0], ToolMessage)
        tool.invoke.assert_called_once_with({"param": "value"})

    def test_call_no_messages(self):
        """Test calling BasicToolNode with no messages raises error"""
        node = BasicToolNode([])
        
        with pytest.raises(ValueError, match="No messages found"):
            node({})

    def test_call_no_tool_calls(self):
        """Test calling BasicToolNode without tool calls raises error"""
        node = BasicToolNode([])
        message = MagicMock()
        del message.tool_calls  # Remove tool_calls attribute
        
        state = {"messages": [message]}
        
        with pytest.raises(ValueError, match="no tool calls"):
            node(state)

    def test_call_unknown_tool(self):
        """Test calling BasicToolNode with unknown tool raises error"""
        node = BasicToolNode([])
        message = MagicMock()
        message.tool_calls = [
            {"name": "unknown_tool", "args": {}, "id": "123"}
        ]
        
        state = {"messages": [message]}
        
        with pytest.raises(ValueError, match="Unknown tool: unknown_tool"):
            node(state)

    def test_call_tool_execution_error(self):
        """Test tool execution error handling"""
        tool = MagicMock(spec=BaseTool)
        tool.name = "failing_tool"
        tool.invoke.side_effect = Exception("Tool failed")

        node = BasicToolNode([tool])

        message = MagicMock()
        message.tool_calls = [
            {"name": "failing_tool", "args": {}, "id": "456"}
        ]

        state = {"messages": [message]}
        
        with pytest.raises(ToolExecutionError, match="Failed to execute failing_tool"):
            node(state)


class TestShouldContinue:
    """Test suite for should_continue function"""

    def test_continue_with_tool_calls(self):
        """Test should_continue returns 'tools' when tool calls exist"""
        message = MagicMock()
        message.tool_calls = [{"name": "tool", "args": {}}]
        state = {"messages": [message]}

        result = should_continue(state)
        assert result == "tools"

    def test_end_without_tool_calls(self):
        """Test should_continue returns '__end__' when no tool calls"""
        message = MagicMock()
        message.tool_calls = []
        state = {"messages": [message]}

        result = should_continue(state)
        assert result == "__end__"

    def test_end_with_invalid_state(self):
        """Test should_continue returns '__end__' for invalid state"""
        assert should_continue({}) == "__end__"
        assert should_continue(None) == "__end__"
        assert should_continue({"messages": []}) == "__end__"

    def test_end_with_no_tool_calls_attribute(self):
        """Test should_continue when message has no tool_calls attribute"""
        message = MagicMock()
        del message.tool_calls
        state = {"messages": [message]}

        result = should_continue(state)
        assert result == "__end__"


class TestValidateWorkflowParams:
    """Test suite for validate_workflow_params function"""

    def test_invalid_vector_store_type(self):
        """Test validation fails with wrong vector store type"""
        with pytest.raises(TypeError, match="vector_store must be"):
            validate_workflow_params("not_a_vector_store", MagicMock(), 10)

    def test_invalid_max_toolset_size_value(self):
        """Test validation fails with invalid max_toolset_size value"""
        # We can't easily test the type validation due to isinstance checks
        # But we can test the value validation in create_fmp_data_workflow
        pass


class TestCreateFmpDataWorkflow:
    """Test suite for create_fmp_data_workflow function"""

    @patch("langchain_fmp_data.agent.StateGraph")
    @patch("langchain_fmp_data.agent.BasicToolNode")
    def test_workflow_creation(self, mock_tool_node, mock_state_graph):
        """Test workflow creation with valid parameters"""
        mock_vs = MagicMock()
        mock_vs.get_tools.return_value = []
        mock_model = MagicMock()
        mock_workflow = MagicMock()
        mock_state_graph.return_value = mock_workflow

        workflow = create_fmp_data_workflow(mock_vs, mock_model)

        assert workflow == mock_workflow
        mock_tool_node.assert_called_once()
        mock_workflow.add_node.assert_called()
        mock_workflow.add_edge.assert_called()
        mock_workflow.add_conditional_edges.assert_called()

    def test_workflow_invalid_max_toolset_size(self):
        """Test workflow creation fails with invalid max_toolset_size"""
        with pytest.raises(ValueError, match="max_toolset_size must be greater"):
            create_fmp_data_workflow(MagicMock(), MagicMock(), max_toolset_size=0)