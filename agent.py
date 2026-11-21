import requests
from typing import Annotated, TypedDict
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt

GUEST_LIST = []

@tool
def get_public_holidays(country_code: str, year: int = 2026) -> str:
    """Get official public holidays for a given country code (e.g., 'GE' for Georgia, 'US' for USA) and year."""
    url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/{country_code.upper()}"
    response = requests.get(url, timeout=15)
    if response.status_code != 200:
        return f"Could not find holidays for country code '{country_code}'."
    holidays = response.json()
    formatted = [f"{h['date']}: {h['localName']} ({h['name']})" for h in holidays[:8]]
    return "\n".join(formatted)

@tool
def get_city_weather(latitude: float = 41.72, longitude: float = 44.79) -> str:
    """Get current temperature and wind speed for given coordinates. Defaults to Tbilisi (41.72, 44.79)."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m"
    }
    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    current = response.json()["current"]
    return f"Temperature: {current['temperature_2m']}°C, Wind speed: {current['wind_speed_10m']} km/h"

@tool
def add_guest(name: str) -> str:
    """Add a guest's name to the event guest list."""
    if name not in GUEST_LIST:
        GUEST_LIST.append(name)
        return f"Guest '{name}' added to the list."
    return f"Guest '{name}' is already on the list."

@tool
def list_guests() -> str:
    """Return all guests currently on the event guest list."""
    if not GUEST_LIST:
        return "The guest list is currently empty."
    return "Current guests: " + ", ".join(GUEST_LIST)

@tool
def remove_guest(name: str) -> str:
    """Remove a guest from the event guest list. Requires human approval before deleting."""
    approved = interrupt(f"Are you sure you want to remove '{name}' from the guest list?")
    if approved:
        for guest in list(GUEST_LIST):
            if guest.lower() == name.strip().lower():
                GUEST_LIST.remove(guest)
                return f"Approved: Guest '{guest}' has been removed."
        return f"Approved, but guest '{name}' was not found on the list."
    else:
        return f"Denied: Action cancelled. '{name}' remains on the list."

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

def build_graph():
    tools = [get_public_holidays, get_city_weather, add_guest, list_guests, remove_guest]
    llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)
    llm_with_tools = llm.bind_tools(tools)

    system_prompt = SystemMessage(
        content="You are a helpful Event & Holiday Organizer Assistant. "
                "Use your tools to check public holidays, check weather, and manage the event guest list. "
                "IMPORTANT: When the user asks to remove or delete a guest, DO NOT ask for confirmation in text. "
                "Immediately call the `remove_guest` tool directly — the tool itself handles human confirmation. "
                "Always reply clearly and politely in the user's language (Georgian or English)."
    )

    def assistant_node(state: AgentState):
        response = llm_with_tools.invoke([system_prompt] + state["messages"])
        return {"messages": [response]}

    builder = StateGraph(AgentState)
    builder.add_node("assistant", assistant_node)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)
    builder.add_edge("tools", "assistant")

    memory = InMemorySaver()
    return builder.compile(checkpointer=memory)
