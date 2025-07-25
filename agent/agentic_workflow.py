from utils.model_loader import ModelLoader
from prompt_library.prompt import SYSTEM_PROMPT
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculator_tool import CalculatorTool
from tools.currency_conversion_tool import CurrencyConverterTool
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

# Define your own MessageState
class MessageState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

class GraphBuilder:
    def __init__(self, model_provider: str = "groq"):
        self.model_loader = ModelLoader(model_provider=model_provider)
        self.llm = self.model_loader.load_llm()
        
        self.tools = []
        
        self.weather_tools = WeatherInfoTool()
        self.place_search_tools = PlaceSearchTool()
        self.calculator_tools = CalculatorTool()
        self.currency_converter_tools = CurrencyConverterTool()
        
        self.tools.extend([
            *self.weather_tools.weather_tool_list,
            *self.place_search_tools.place_search_tool_list,
            *self.calculator_tools.calculator_tool_list,
            *self.currency_converter_tools.currency_converter_tool_list
        ])
        
        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)
        
        self.graph = None
        
        self.system_prompt = SYSTEM_PROMPT

    def agent_function(self, state: MessageState):
        """Main agent function"""
        # Fixed: Changed from 'message' to 'messages' (plural)
        user_messages = state["messages"]
        
        # Create input with system prompt and user messages
        input_messages = [self.system_prompt] + user_messages
        
        response = self.llm_with_tools.invoke(input_messages)
        return {"messages": [response]}

    def build_graph(self):
        graph_builder = StateGraph(MessageState)
        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        
        graph_builder.add_edge(START, "agent")
        
        # Fixed: Changed from 'add_conditional_edgea' to 'add_conditional_edges'
        graph_builder.add_conditional_edges("agent", tools_condition)
        
        # Better approach: Add conditional edge from tools back to agent or END
        graph_builder.add_edge("tools", "agent")
        # Alternative: graph_builder.add_conditional_edges("tools", tools_condition)
        
        self.graph = graph_builder.compile()
        return self.graph

    def __call__(self):
        return self.build_graph()