from crewai import Crew, Process
from agents.researcher_agent import create_researcher_agent
from agents.writer_agent import create_writer_agent
from tasks.research_task import create_research_task
from tasks.writing_task import create_writing_task
from memory.search_history import save_memory, get_memory_context
from tools.docx_exporter import export_to_docx
import os

def run_manufacturing_crew(query: str):
    print(f"\n🏭 Multi-Agent Manufacturing System Started")
    print(f"📋 Query: {query}")

    # Show memory context
    memory_ctx = get_memory_context()
    print(f"\n🧠 Memory Context:\n{memory_ctx}")
    print("=" * 60)

    # Create agents
    researcher = create_researcher_agent()
    writer = create_writer_agent()

    # Create tasks
    research_task = create_research_task(researcher, query)
    writing_task = create_writing_task(writer)
    writing_task.context = [research_task]

    # Assemble crew
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task],
        process=Process.sequential,
        verbose=True
    )

    # Run
    result = crew.kickoff()
    result_str = str(result)

    # ── Save outputs ───────────────────────────────────────
    os.makedirs("outputs", exist_ok=True)

    # 1. Save Markdown
    md_path = "outputs/procurement_report.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(result_str)
    print(f"\n✅ Markdown saved to: {md_path}")

    # 2. Save .docx
    docx_path = "outputs/procurement_report.docx"
    export_to_docx(result_str, query, docx_path)

    # 3. Save to memory
    save_memory(query, result_str)
    print(f"🧠 Query saved to memory for future runs!")

    print("\n" + "=" * 60)
    print(result_str)
    return result_str

if __name__ == "__main__":
    # ── Dynamic query input ────────────────────────────────
    print("🏭 Welcome to the Multi-Agent Manufacturing System")
    print("=" * 60)
    query = input("🔍 Enter your manufacturing research query: ").strip()

    if not query:
        query = "Find top suppliers for industrial-grade aluminum sheets for manufacturing"
        print(f"Using default query: {query}")

    run_manufacturing_crew(query)