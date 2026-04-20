from crewai import Task

def create_writing_task(agent, research_context: str = None):
    task = Task(
        description=(
            "Using the supplier research provided, write a professional "
            "Manufacturing Procurement Report.\n\n"
            "The report MUST include:\n"
            "1. Executive Summary (2-3 sentences overview)\n"
            "2. Supplier Comparison Table (Name | Pricing | Lead Time | Certifications | Rating)\n"
            "3. Detailed Supplier Profiles (one section per supplier)\n"
            "4. Top Recommendation with justification\n"
            "5. Risk Assessment (supply chain risks, single-source risk, etc.)\n"
            "6. Next Steps / Action Items\n\n"
            "Format the report in clean Markdown. "
            "Be professional, concise, and actionable."
        ),
        expected_output=(
            "A complete, professional Markdown procurement report with all 6 sections, "
            "ready to be shared with a procurement manager."
        ),
        agent=agent,
        context_from_async_tasks_callback=None
    )
    return task