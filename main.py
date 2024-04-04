"""Example LangChain server exposes and agent that has conversation history.

In this example, the history is stored entirely on the client's side.

Please see other examples in LangServe on how to use RunnableWithHistory to
store history on the server side.

Relevant LangChain documentation:

* Creating a custom agent: https://python.langchain.com/docs/modules/agents/how_to/custom_agent
* Streaming with agents: https://python.langchain.com/docs/modules/agents/how_to/streaming#custom-streaming-with-events
* General streaming documentation: https://python.langchain.com/docs/expression_language/streaming
* Message History: https://python.langchain.com/docs/expression_language/how_to/message_history

**ATTENTION**
1. To support streaming individual tokens you will need to use the astream events
   endpoint rather than the streaming endpoint.
2. This example does not truncate message history, so it will crash if you
   send too many messages (exceed token length).
3. The playground at the moment does not render agent output well! If you want to
   use the playground you need to customize it's output server side using astream
   events by wrapping it within another runnable.
4. See the client notebook it has an example of how to use stream_events client side!
"""  # noqa: E501
from dotenv import load_dotenv
from typing import Any, List, Union

from fastapi import FastAPI
from langchain.agents import AgentExecutor, tool
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.prompts import MessagesPlaceholder
from langchain_community.tools.convert_to_openai import format_tool_to_openai_tool
from langchain_core.messages import AIMessage, FunctionMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from reactors.pfr.tools import PlugFlowConversionTool
from reactors.pfr.molar_expansion import pfr_expansion_factor
from reactors.pfr.tools import PlugFlowVolumeConversionTool
from scipy.optimize import fsolve

from fastapi.middleware.cors import CORSMiddleware

from langserve import add_routes
from langserve.pydantic_v1 import BaseModel, Field



load_dotenv()

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are very powerful assistant, but bad at calculating conversion of a reaction. "
            "Talk with the user as normal. "
            "If they ask you to calculate the conversion of a reactor, use the pfr_conversion tool. If they ask you to calculate the volume, use the pfr_expansion_volume_conversion tool.",
        ),
        # Please note the ordering of the fields in the prompt!
        # The correct ordering is:
        # 1. history - the past messages between the user and the agent
        # 2. user - the user's current input
        # 3. agent_scratchpad - the agent's working space for thinking and
        #    invoking tools to respond to the user's input.
        # If you change the ordering, the agent will not work correctly since
        # the messages will be shown to the underlying LLM in the wrong order.
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


@tool
def word_length(word: str) -> int:
    """Returns a counter word"""
    return len(word)

@tool
def pfr_conversion(v_0, T, P_0, c_A0, c_B0, k, V):
    """Returns the conversion"""
    conv, prod = pfr_expansion_factor(v_0, T, P_0, c_A0, c_B0, k, V)
    # plug_flow_conversion_dict = {
    #     "initial_volumetric_flowrate": v_0,
    #     "temperature": T,
    #     "initial_pressure": P_0,
    #     "initial_concentration_of_A": c_A0,
    #     "initial_concentration_of_B": c_B0,
    #     "rate_constant": k,
    #     "reactor_volume": V,
    #     "conversion": conv,
    # }
    return float(conv)

@tool
def pfr_expansion_volume_conversion(v_0, T, P_0, c_A0, c_B0, k, X):
    """
    Find the reactor volume needed to achieve a target conversion of A.

    Parameters:
    - X: Desired conversion of A (0 to 1)
    - v_0: Initial volumetric flow rate
    - T: Temperature
    - P_0: Initial Pressure
    - c_A0: Initial Concentration of A
    - c_B0: Initial Concentration of B
    - k: Rate Constant
    - V_max: Maximum reactor volume to consider

    Returns:
    - V: Reactor volume that achieves the target conversion
    """
    def objective(V):
        conv_calc, prod_calc = pfr_expansion_factor(v_0, T, P_0, c_A0, c_B0, k, V)
        return conv_calc - X

    v_solve = fsolve(objective, 1)[0]
    # plug_flow_conversion_dict = {
    #     "initial_volumetric_flowrate": v_0,
    #     "temperature": T,
    #     "initial_pressure": P_0,
    #     "initial_concentration_of_A": c_A0,
    #     "initial_concentration_of_B": c_B0,
    #     "rate_constant": k,
    #     "reactor_volume": v_solve,
    #     "conversion": X,
    # }
    return v_solve

# We need to set streaming=True on the LLM to support streaming individual tokens.
# Tokens will be available when using the stream_log / stream events endpoints,
# but not when using the stream endpoint since the stream implementation for agent
# streams action observation pairs not individual tokens.
# See the client notebook that shows how to use the stream events endpoint.
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, streaming=True)

tools = [pfr_conversion, pfr_expansion_volume_conversion]


llm_with_tools = llm.bind(tools=[format_tool_to_openai_tool(tool) for tool in tools])

# ATTENTION: For production use case, it's a good idea to trim the prompt to avoid
#            exceeding the context window length used by the model.
#
# To fix that simply adjust the chain to trim the prompt in whatever way
# is appropriate for your use case.
# For example, you may want to keep the system message and the last 10 messages.
# Or you may want to trim based on the number of tokens.
# Or you may want to also summarize the messages to keep information about things
# that were learned about the user.
#
# def prompt_trimmer(messages: List[Union[HumanMessage, AIMessage, FunctionMessage]]):
#     '''Trims the prompt to a reasonable length.'''
#     # Keep in mind that when trimming you may want to keep the system message!
#     return messages[-10:] # Keep last 10 messages.

# def custom_output_parser():
#     # Extract the relevant output from the agent's response
#     # Assuming the conversion result is directly the output of the tool
#     output = OpenAIToolsAgentOutputParser()
#     content = output["messages"][0]["content"]
#     return content

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
        "chat_history": lambda x: x["chat_history"],
    }
    | prompt
    # | prompt_trimmer # See comment above.
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using LangChain's Runnable interfaces",
)


# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# We need to add these input/output schemas because the current AgentExecutor
# is lacking in schemas.
class Input(BaseModel):
    input: str
    # The field extra defines a chat widget.
    # Please see documentation about widgets in the main README.
    # The widget is used in the playground.
    # Keep in mind that playground support for agents is not great at the moment.
    # To get a better experience, you'll need to customize the streaming output
    # # for now.
    chat_history: List[Union[HumanMessage, AIMessage, FunctionMessage]] = Field(
        ...,
        extra={"widget": {"type": "chat", "input": "input", "output": "output"}},
    )


class Output(BaseModel):
    output: Any


# Adds routes to the app for using the chain under:
# /invoke
# /batch
# /stream
# /stream_events
add_routes(
    app,
    agent_executor.with_types(input_type=Input, output_type=Output).with_config(
        {"run_name": "agent"}
    ),
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)

