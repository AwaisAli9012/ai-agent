import os
import streamlit as st
from groq import Groq
from ddgs import DDGS
import wikipediaapi
import math

# Load API key
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ── TOOLS ──────────────────────────────────────────────

def web_search(query):
    """Search the web using DuckDuckGo"""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        if results:
            output = ""
            for r in results:
                output += f"Title: {r['title']}\n"
                output += f"Summary: {r['body']}\n\n"
            return output
        return "No results found."
    except Exception as e:
        return f"Web search error: {str(e)}"

def wikipedia_search(query):
    """Search Wikipedia for information"""
    try:
        # Clean the query — remove common question words
        clean = query.lower()
        for word in ["who is", "what is", "tell me about", "explain", "who was", "what are"]:
            clean = clean.replace(word, "").strip()
        
        wiki = wikipediaapi.Wikipedia('ai-agent', 'en')
        page = wiki.page(clean.title())
        if page.exists():
            return page.summary[:500]
        return f"No Wikipedia page found for: {clean}"
    except Exception as e:
        return f"Wikipedia error: {str(e)}"

def calculator(expression):
    """Calculate a math expression"""
    try:
        result = eval(expression, {"__builtins__": {}}, {"math": math})
        return f"Result: {result}"
    except Exception as e:
        return f"Calculator error: {str(e)}"

# ── AGENT LOGIC ────────────────────────────────────────

def run_agent(user_input):
    query = user_input.lower()

    # Check web search FIRST before calculator
    if any(word in query for word in ["weather", "news", "today", "latest", "current", "price", "score", "stock"]):
        tool_result = web_search(user_input)
        tool_name = "web_search"

    elif any(word in query for word in ["calculate", "+", "-", "*", "/", "sqrt", "percent", "multiply", "divided", "plus", "minus"]):
        tool_result = calculator(user_input)
        tool_name = "calculator"

    else:
        tool_result = wikipedia_search(user_input)
        tool_name = "wikipedia_search"

    # Send tool result to LLM for a clean final answer
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Use the provided information to answer the user's question clearly."},
        {"role": "user", "content": f"Question: {user_input}\n\nInformation: {tool_result}"}
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    return response.choices[0].message.content, tool_name

# ── STREAMLIT UI ───────────────────────────────────────

st.set_page_config(page_title="AI Agent", page_icon="🤖")
st.title("🤖 AI Agent")
st.write("Ask me anything — I can search the web, look up Wikipedia, or calculate math!")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
user_input = st.chat_input("Ask me anything...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer, tool_used = run_agent(user_input)
                if tool_used:
                    st.caption(f"🔧 Tool used: {tool_used}")
                st.write(answer)
            except Exception as e:
                answer = "Sorry, I ran into an issue. Please try rephrasing your question."
                st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})