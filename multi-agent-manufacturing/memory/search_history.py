import json
import os
from datetime import datetime

MEMORY_FILE = "memory/search_history.json"

def load_memory() -> dict:
    """Load past search history from file."""
    if not os.path.exists(MEMORY_FILE):
        return {"searches": []}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:          # ✅ handles empty file
            return {"searches": []}
        return json.loads(content)


def save_memory(query: str, summary: str):
    """Save a new search entry to memory."""
    memory = load_memory()
    memory["searches"].append({
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "summary": summary[:300]  # store first 300 chars as summary
    })
    os.makedirs("memory", exist_ok=True)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

def get_memory_context() -> str:
    """Return past searches as a readable context string for agents."""
    memory = load_memory()
    if not memory["searches"]:
        return "No previous searches found."
    
    context = "=== PAST SEARCH HISTORY ===\n"
    for i, entry in enumerate(memory["searches"][-5:], 1):  # last 5 searches
        context += f"\n[{i}] Date: {entry['timestamp'][:10]}\n"
        context += f"    Query: {entry['query']}\n"
        context += f"    Summary: {entry['summary']}\n"
    return context