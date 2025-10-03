import json
from typing import Any, Dict, List

# Try Google ADK; if unavailable, use a tiny local shim so hackathon demo still runs.
try:
    from adk import Agent
    ADK_AVAILABLE = True
except Exception:
    ADK_AVAILABLE = False

from .tools import perform_batch_matching

class _ShimAgent:
    """Local fallback that behaves like a minimal ADK Agent."""
    def __init__(self, instructions: str = ""):
        self.instructions = instructions

    def run(self, message: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
        # For our use-case, just run the batch and return structured JSON
        results = perform_batch_matching()
        return {
            "message": "Batch matching complete.",
            "count": len(results),
            "results": results
        }

class FoodMatchAgent(Agent if ADK_AVAILABLE else _ShimAgent):
    def __init__(self):
        super().__init__(
            instructions=(
                "You are a Smart City food redistribution coordinator. "
                "When invoked, read CSVs for restaurants, NGOs, and volunteers, "
                "match donations to NGO requests by priority and distance, "
                "assign the nearest available volunteer, and log results."
            )
        )

    # If ADK is present, override run to call the same batch function
    def run(self, message: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:  # type: ignore[override]
        results = perform_batch_matching()
        return {
            "message": "Batch matching complete.",
            "count": len(results),
            "results": results
        }

if __name__ == "__main__":
    agent = FoodMatchAgent()
    out = agent.run("Run batch matching")
    print("\n=== AGENT OUTPUT (summary) ===")
    print(json.dumps({"count": out["count"]}, indent=2))
    # If you want full detail in terminal, uncomment:
    # print(json.dumps(out, indent=2))
    print("Wrote/updated logs at food_match_agent/logs/logs.json")
