from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentType, initialize_agent
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from reactors.pfr.tools import PlugFlowConversionTool
# Load OpenAI API Key from .env file
load_dotenv()


# Initialize agent
def init_agent(model):
    llm = ChatOpenAI(
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()],
        model=model
    )
    tools = [
        PlugFlowConversionTool(),
    ]
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS
    )
    return agent


agent = init_agent(model='gpt-3.5-turbo-0613')

query = input("\nEnter your question here (Type 'exit' to end):")

agent(query)