import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

def get_llm():
    return LLM(
        model="groq/llama-3.3-70b-versatile",   # ✅ CrewAI format: provider/model
        api_key=os.getenv("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"),
        temperature=0.3,
        max_tokens=4096
    )