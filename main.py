import os
import getpass
from langgraph.types import Command
from agent import build_graph

def main():
    if not os.environ.get("GROQ_API_KEY"):
        os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your GROQ_API_KEY: ")

    graph = build_graph()
    config = {"configurable": {"thread_id": "cli-session-1"}}

    print("=== Event & Holiday Organizer Agent (CLI) ===")
    print("ჩაწერეთ შეტყობინება (გასასვლელად აკრიფეთ 'exit'):\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("ნახვამდის!")
            break
        if not user_input:
            continue

        result = graph.invoke({"messages": [("user", user_input)]}, config)
        state = graph.get_state(config)

        if state.tasks and state.tasks[0].interrupts:
            question = state.tasks[0].interrupts[0].value
            print(f"\n⚠️ {question}")
            confirm = input("დაადასტურეთ (yes/no): ").strip().lower()
            approved = confirm in ["yes", "y", "დიახ", "კი"]
            result = graph.invoke(Command(resume=approved), config)

        print(f"Agent: {result['messages'][-1].content}\n")

if __name__ == "__main__":
    main()
