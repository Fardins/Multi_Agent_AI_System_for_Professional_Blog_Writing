import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Primary writer — slightly lower temp for consistency, still creative
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0.65,
    max_tokens=8192,
)

# Planning + SEO — needs precise structured JSON
llm_plan = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0.2,
    max_tokens=2048,
)

# Synthesis/analysis — reads evidence and extracts key facts
llm_analyst = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0.1,
    max_tokens=4096,
)

# Fast model for lightweight tasks
llm_fast = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant",
    temperature=0.2,
    max_tokens=1024,
)