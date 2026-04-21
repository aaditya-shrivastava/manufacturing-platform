from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from langchain_community.tools import DuckDuckGoSearchRun

def get_search_tool():
    # Free - no API key needed
    search = DuckDuckGoSearchRun()
    return search