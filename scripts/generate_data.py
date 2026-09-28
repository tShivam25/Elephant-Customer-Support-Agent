import json
import random

def generate_customers():
    customers = [
        {
            "id": "hero_priya",
            "name": "Priya Nair",
            "company": "DesignSync",
            "plan": "Pro",
            "environment": "Mac, QuickBooks",
            "preference": "email",
            "tone": "mildly frustrated",
            "tickets": [
                {
                    "date": "10 days ago",
                    "issue": "Invoice sync to QuickBooks failed",
                    "fix_attempted": "Reconnect integration",
                    "outcome": "failed",
                    "sentiment": "neutral"
                },
                {
                    "date": "2 days ago",
                    "issue": "Invoice sync to QuickBooks failed",
                    "fix_attempted": "Clear cache",
                    "outcome": "failed",
                    "sentiment": "mildly frustrated"
                }
            ]
        },
        {
            "id": "cust_01",
            "name": "Alex Mercer",
            "company": "TechNova",
            "plan": "Enterprise",
            "environment": "Windows, NetSuite",
            "preference": "slack",
            "tone": "direct",
            "tickets": [
                {
                    "date": "30 days ago",
                    "issue": "API rate limit exceeded",
                    "fix_attempted": "Increase rate limit temporarily",
                    "outcome": "worked",
                    "sentiment": "happy"
                }
            ]
        },
        {
            "id": "cust_02",
            "name": "Sarah Jenkins",
            "company": "BakeShop Inc",
            "plan": "Starter",
            "environment": "Windows, Xero",
            "preference": "phone",
            "tone": "friendly",
            "tickets": [
                {
                    "date": "15 days ago",
                    "issue": "Duplicate charges on invoice",
                    "fix_attempted": "Refund duplicate",
                    "outcome": "worked",
                    "sentiment": "relieved"
                }
            ]
        }
    ]
    # Add a few more generic customers to hit ~10
    names = ["John Doe", "Jane Smith", "Alice Johnson", "Bob Williams", "Charlie Brown", "Diana Prince", "Eve Adams"]
    companies = ["Acme Corp", "Globex", "Initech", "Umbrella Corp", "Stark Ind", "Wayne Ent", "Wonka Ind"]
    plans = ["Starter", "Pro", "Enterprise"]
    envs = ["Windows, Xero", "Mac, QuickBooks", "Windows, NetSuite", "Linux, Custom ERP"]
    prefs = ["email", "phone", "slack"]
    tones = ["polite", "frustrated", "urgent", "casual"]
    issues = ["Login SSO failed", "Export errors to CSV", "Tax settings incorrect", "Refund processing error"]

    for i in range(7):
        cust = {
            "id": f"cust_{i+3:02d}",
            "name": names[i],
            "company": companies[i],
            "plan": random.choice(plans),
            "environment": random.choice(envs),
            "preference": random.choice(prefs),
            "tone": random.choice(tones),
            "tickets": []
        }
        for j in range(random.randint(1, 3)):
            cust["tickets"].append({
                "date": f"{random.randint(2, 30)} days ago",
                "issue": random.choice(issues),
                "fix_attempted": "Standard troubleshooting",
                "outcome": random.choice(["worked", "failed"]),
                "sentiment": random.choice(["neutral", "frustrated", "happy"])
            })
        customers.append(cust)
    return customers

if __name__ == "__main__":
    customers = generate_customers()
    with open("../data/customers.json", "w") as f:
        json.dump(customers, f, indent=2)
