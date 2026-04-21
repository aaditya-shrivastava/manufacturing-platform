from crewai import Agent
from crewai.tools import BaseTool
from config import get_llm
from ddgs import DDGS
from pydantic import BaseModel, Field
from memory.search_history import get_memory_context

class WebSearchInput(BaseModel):
    query: str = Field(description="Search query to look up suppliers and manufacturing data")

class WebSearchTool(BaseTool):
    name: str = "Web Search Tool"
    description: str = "Search the web for information about suppliers, pricing, and manufacturing data."
    args_schema: type[BaseModel] = WebSearchInput

    def _run(self, query: str) -> str:
        results = DDGS().text(query, max_results=5)
        output = ""
        for r in results:
            output += f"Title: {r['title']}\nURL: {r['href']}\nSummary: {r['body']}\n\n"
        return output if output else "No results found."

def create_researcher_agent():
    llm = get_llm()
    search_tool = WebSearchTool()
    memory_context = get_memory_context()

    researcher = Agent(
        role="Manufacturing Researcher",
        goal=(
            "Find detailed, accurate information about suppliers, "
            "materials, pricing, and lead times for manufacturing needs. "
            "Use past search history to avoid repeating research and build on prior findings."
        ),
        backstory=(
            "You are an expert manufacturing procurement researcher with "
            "10+ years of experience sourcing industrial suppliers globally. "
            "You maintain a research memory to improve results over time.\n\n"
            f"{memory_context}"
        ),
        tools=[search_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )

    return researcher