import os 
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


system_prompt="Act as an AI chatbot who is smart and friendly."
from langchain_groq.chat_models import ChatGroq
from langchain_openai import OpenAI, ChatOpenAI
from langchain_tavily import TavilySearch
from langchain_core.messages.ai import AIMessage


openai_llm =ChatOpenAI(model="gpt-4o-mini")
groq_llm =ChatGroq(model="llama-3.3-70b-versatile")

search_tool = TavilySearch(max_results=2)

from langgraph.prebuilt import create_react_agent

# Mapping of allowed Groq models (add/alias as needed)
GROQ_MODEL_MAP = {
    "llama3-70b-8192": "llama3-70b-8192",
    "llama3-8b-8192": "llama3-8b-8192",
    "mixtral-8x7b-32768": "mixtral-8x7b-32768",
    # Example alias:
    # "llama3-70b-versatile": "llama3-70b-8192",
}

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    # Select LLM based on provider and validate model names
    if provider.lower() == "groq":
        if llm_id not in GROQ_MODEL_MAP:
            raise ValueError(f"Model '{llm_id}' not available for Groq. Allowed: {list(GROQ_MODEL_MAP.keys())}")
        llm = ChatGroq(model=GROQ_MODEL_MAP[llm_id])
    elif provider.lower() == "openai":
        llm = ChatOpenAI(model=llm_id)
    else:
        raise ValueError("Provider not supported")

    # Select tools based on allow_search
    tools = [TavilySearch(max_results=2)] if allow_search else []

    # Create agent with system_prompt as state_modifier
    agent = create_react_agent(
        model=llm,
        tools=tools
    )

    # Ensure query is a list of strings
    if isinstance(query, str):
        user_messages = [query]
    elif isinstance(query, list):
        user_messages = query
    else:
        user_messages = [str(query)]

    state = {
        "messages": [{"role": "system", "content": system_prompt}] +
                    [{"role": "user", "content": m} for m in user_messages]
    }
    response = agent.invoke(state)
    messages = response.get("messages")
    ai_messages = [message.content for message in messages if isinstance(message, AIMessage)]
    return ai_messages[-1] if ai_messages else None

# Example usage
query = "Tell me about the trends in crypto market"
response = get_response_from_ai_agent("gpt-4o-mini", query, False, system_prompt, "openai")
print(response)
