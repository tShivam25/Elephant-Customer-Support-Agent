import json
import os
from typing import Dict, Any, List

def load_data(filename: str) -> Any:
    path = os.path.join(os.path.dirname(__file__), "..", "data", filename)
    with open(path, "r") as f:
        return json.load(f)

def lookup_customer(customer_id: str) -> Dict[str, Any]:
    """Retrieve customer details by ID."""
    customers = load_data("customers.json")
    for c in customers:
        if c["id"] == customer_id:
            return c
    return {"error": "Customer not found"}

def search_kb(query: str) -> List[Dict[str, str]]:
    """Search the Knowledge Base for articles matching the query."""
    kb = load_data("kb_articles.json")
    results = []
    q = query.lower()
    for article in kb:
        if q in article["title"].lower() or q in article["content"].lower():
            results.append(article)
    return results

def check_invoice_status(invoice_id: str) -> Dict[str, Any]:
    """Check the status of a specific invoice."""
    db = load_data("mock_db.json")
    for inv in db.get("invoices", []):
        if inv["id"] == invoice_id:
            return inv
    return {"error": "Invoice not found"}

def check_service_status() -> Dict[str, Any]:
    """Check the current system status for active incidents."""
    db = load_data("mock_db.json")
    return db.get("status_page", {"active_incident": False})

def create_ticket(customer_id: str, issue: str) -> Dict[str, Any]:
    """Create a new support ticket."""
    return {"status": "success", "ticket_id": f"TKT-{hash(customer_id + issue) % 10000}", "message": "Ticket created successfully"}

def escalate_to_human(customer_id: str, brief: str) -> Dict[str, Any]:
    """Escalate the conversation to a human agent, providing a brief summary of the issue."""
    return {"status": "success", "action": "escalated", "message": "Escalated to human tier-2 support with brief.", "brief": brief}

def draft_email(customer_id: str, content: str) -> Dict[str, Any]:
    """Draft an email to the customer with the provided content."""
    return {"status": "success", "action": "email_drafted", "content": content}

# List of tool definitions for Groq API
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "lookup_customer",
            "description": "Retrieve customer details (plan, environment, preferences) by customer_id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string"}
                },
                "required": ["customer_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_kb",
            "description": "Search the Knowledge Base for troubleshooting steps and articles.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Keywords to search the KB for."}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_invoice_status",
            "description": "Check the status of a specific invoice by ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "invoice_id": {"type": "string"}
                },
                "required": ["invoice_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_service_status",
            "description": "Check if there are any active system-wide incidents or outages.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_ticket",
            "description": "Create a new standard support ticket for a customer issue.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string"},
                    "issue": {"type": "string", "description": "Description of the issue."}
                },
                "required": ["customer_id", "issue"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "escalate_to_human",
            "description": "Escalate the issue to a human agent when automated fixes fail or customer is highly frustrated.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string"},
                    "brief": {"type": "string", "description": "A concise summary of the issue, what was tried, and why it's escalated."}
                },
                "required": ["customer_id", "brief"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "draft_email",
            "description": "Draft an email response to the customer (if they prefer email communication).",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string"},
                    "content": {"type": "string", "description": "The body of the email."}
                },
                "required": ["customer_id", "content"]
            }
        }
    }
]

def execute_tool(name: str, arguments: Dict[str, Any]) -> Any:
    if name == "lookup_customer":
        return lookup_customer(**arguments)
    elif name == "search_kb":
        return search_kb(**arguments)
    elif name == "check_invoice_status":
        return check_invoice_status(**arguments)
    elif name == "check_service_status":
        return check_service_status(**arguments)
    elif name == "create_ticket":
        return create_ticket(**arguments)
    elif name == "escalate_to_human":
        return escalate_to_human(**arguments)
    elif name == "draft_email":
        return draft_email(**arguments)
    else:
        return {"error": f"Unknown tool: {name}"}
