from crewai import Agent
from config import get_llm

def create_writer_agent():
    llm = get_llm()

    writer = Agent(
        role="Manufacturing Report Writer",
        goal=(
            "Transform raw research data into professional, well-structured "
            "manufacturing procurement reports that are clear, actionable, and executive-ready."
        ),
        backstory=(
            "You are a senior technical writer specializing in manufacturing and procurement. "
            "You have written hundreds of supplier evaluation reports for Fortune 500 companies. "
            "You excel at turning raw data into polished, scannable documents with clear "
            "recommendations and risk assessments."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
        tools=[]  # Writer only synthesizes — no search tools needed
    )

    return writer