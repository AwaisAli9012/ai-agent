# AI Agent — Intelligent Question Answering System

A conversational AI agent that autonomously selects and uses tools to answer user questions. Built with Python, Streamlit, and Meta's LLaMA 3.3 via Groq API.

## Overview

Unlike a standard chatbot that relies purely on its training data, this agent decides which tool to use based on the user's question and fetches real, accurate information before generating an answer.

**Tools available to the agent:**
- **Web Search** — retrieves current information from the web using DuckDuckGo
- **Wikipedia** — fetches factual summaries for people, places, events, and concepts
- **Calculator** — evaluates mathematical expressions with safety restrictions

## Demo

![AI Agent Demo](demo.png)

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.11 |
| UI Framework | Streamlit |
| LLM | LLaMA 3.3-70b-versatile |
| LLM Provider | Groq API |
| Web Search | DuckDuckGo (ddgs) |
| Knowledge Base | Wikipedia API |
| Environment | python-dotenv |

## Architecture
User Question
│
▼
Keyword Router
│
├── Weather/News/Current → Web Search
├── Math/Calculate       → Calculator
└── Everything else      → Wikipedia
│
▼
Tool Result
│
▼
LLaMA 3.3 (Groq)
│
▼
Final Answer

## Getting Started

### Prerequisites
- Python 3.11
- Anaconda
- Groq API key (free at console.groq.com)

### Installation

```bash
# Clone the repository
git clone https://github.com/AwaisAli9012/ai-agent.git
cd ai-agent

# Create and activate environment
conda create -n ai-agent python=3.11
conda activate ai-agent

# Install dependencies
pip install streamlit groq ddgs wikipedia-api python-dotenv

# Add your API key
echo GROQ_API_KEY=your_key_here > .env

# Run the app
streamlit run agent.py
```

## Project Structure
ai-agent/
├── agent.py        # Core agent logic and Streamlit UI
├── .env            # API keys (excluded from version control)
├── .gitignore      # Prevents sensitive files from being pushed
└── README.md       # Project documentation

## Key Design Decisions

- **No LangChain** — agent logic implemented from scratch for deeper understanding of how tool-calling works
- **Keyword routing** — lightweight and reliable alternative to LLM-driven tool selection
- **Security** — calculator uses restricted eval() to prevent code injection

## Author

**Awais Ali** — AI/ML Engineer  
[GitHub](https://github.com/AwaisAli9012) • [LinkedIn](https://linkedin.com/in/awais-ali-282214279)
