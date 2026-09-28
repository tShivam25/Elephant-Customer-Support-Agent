import os
import json
import asyncio
from backend.agent import run_agent

def run_evaluation():
    print("Running Evaluation: Stateless vs Hindsight Memory")
    
    scenarios = [
        {
            "name": "Repeated Failed Fix",
            "customer_id": "hero_priya",
            "message": "My invoice sync to QuickBooks failed again.",
            "expected_behavior": "Should NOT suggest reconnecting or clearing cache, as those failed previously. Should escalate."
        }
    ]
    
    results = []
    
    for s in scenarios:
        print(f"\nEvaluating Scenario: {s['name']}")
        print(f"User Message: {s['message']}")
        
        print("\n--- Running STATELESS Mode ---")
        stateless_res = run_agent(s["customer_id"], s["message"], use_memory=False)
        print("Reply:", stateless_res["reply"])
        
        print("\n--- Running HINDSIGHT Mode ---")
        hindsight_res = run_agent(s["customer_id"], s["message"], use_memory=True)
        print("Reply:", hindsight_res["reply"])
        print("Memories Used:", hindsight_res["memories"])
        
        results.append({
            "scenario": s["name"],
            "stateless": stateless_res,
            "hindsight": hindsight_res
        })
        
    with open("eval_results.json", "w") as f:
        json.dump(results, f, indent=2)
        
    print("\nEvaluation complete. Results saved to eval_results.json")

if __name__ == "__main__":
    run_evaluation()
