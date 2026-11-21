import os
import uuid
import streamlit as st
from langgraph.types import Command
from agent import build_graph

st.set_page_config(page_title="Event & Holiday Organizer Agent", page_icon="🎉")
st.title("🎉 Event & Holiday Organizer Agent")
st.caption("გეხმარებათ ღონისძიებების დაგეგმვაში: უქმე დღეების შემოწმება, ამინდის პროგნოზი და სტუმრების სიის მართვა.")

# API გასაღების წაკითხვა
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
elif not os.environ.get("GROQ_API_KEY"):
    key = st.sidebar.text_input("შეიყვანეთ GROQ_API_KEY:", type="password")
    if key:
        os.environ["GROQ_API_KEY"] = key

if not os.environ.get("GROQ_API_KEY"):
    st.warning("გასაგრძელებლად შეიყვანეთ GROQ_API_KEY მარცხენა პანელზე ან Streamlit Secrets-ში.")
    st.stop()

# Session State-ის ინიციალიზაცია
if "graph" not in st.session_state:
    st.session_state.graph = build_graph()
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_approval" not in st.session_state:
    st.session_state.pending_approval = None

config = {"configurable": {"thread_id": st.session_state.thread_id}}

# საუბრის ისტორიის ჩვენება
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# თუ აგენტი ელოდება დადასტურებას (interrupt)
if st.session_state.pending_approval:
    st.warning(f"⚠️ დადასტურება: {st.session_state.pending_approval}")
    col1, col2 = st.columns(2)
    if col1.button("✅ დიახ, წაშალე"):
        try:
            res = st.session_state.graph.invoke(Command(resume=True), config)
            reply = res["messages"][-1].content
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.session_state.pending_approval = None
            st.rerun()
        except Exception as e:
            st.error(f"შეცდომა: {e}")
    if col2.button("❌ არა, გააუქმე"):
        try:
            res = st.session_state.graph.invoke(Command(resume=False), config)
            reply = res["messages"][-1].content
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.session_state.pending_approval = None
            st.rerun()
        except Exception as e:
            st.error(f"შეცდომა: {e}")

# მომხმარებლის ახალი შეტყობინება
if prompt := st.chat_input("მომწერეთ შეტყობინება... (მაგ: დაამატე ნინო სიაში)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        res = st.session_state.graph.invoke({"messages": [("user", prompt)]}, config)
        state = st.session_state.graph.get_state(config)
        if state.tasks and state.tasks[0].interrupts:
            st.session_state.pending_approval = state.tasks[0].interrupts[0].value
            st.rerun()
        else:
            reply = res["messages"][-1].content
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.markdown(reply)
    except Exception as e:
        st.error(f"დაფიქსირდა შეცდომა (შეამოწმეთ API Key ან ლიმიტი): {e}")
