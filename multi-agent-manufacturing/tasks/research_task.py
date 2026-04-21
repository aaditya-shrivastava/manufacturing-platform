from crewai import Task

def create_research_task(agent, query: str):
    task = Task(
        description=(
            f"Research the following manufacturing requirement: {query}\n\n"
            "Your research must include:\n"
            "1. At least 3-5 potential suppliers with names and websites\n"
            "2. Estimated pricing or price range\n"
            "3. Key specifications and material grades available\n"
            "4. Approximate lead times\n"
            "5. Any quality certifications (ISO, etc.)\n\n"
            "Be specific and factual. If exact data isn't available, "
            "provide industry-standard estimates."
        ),
        expected_output=(
            "A detailed research report with supplier names, pricing, "
            "specs, lead times, and certifications in a clear structured format."
        ),
        agent=agent
    )
    return task