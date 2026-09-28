import os
import json
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

def seed_hindsight():
    api_key = os.getenv("HINDSIGHT_API_KEY", "")
    base_url = os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io")
    
    if not api_key:
        print("Warning: HINDSIGHT_API_KEY not set. Cannot seed memory. Skipping.")
        return

    # Assuming hindsight_client usage based on docs
    client = Hindsight(api_key=api_key, base_url=base_url)

    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "customers.json")
    with open(data_path, "r") as f:
        customers = json.load(f)

    print(f"Seeding memory for {len(customers)} customers...")
    
    for c in customers:
        bank_id = c["id"]
        # Also store customer profile facts
        profile_fact = f"Customer {c['name']} works at {c['company']}, on the {c['plan']} plan. Environment: {c['environment']}. Preferred contact: {c['preference']}. Tone: {c['tone']}."
        print(f"Retaining profile for {bank_id}...")
        try:
            client.retain(bank_id=bank_id, content=profile_fact)
            
            for t in c["tickets"]:
                ticket_fact = f"Ticket from {t['date']}: Issue was '{t['issue']}'. Fix attempted: '{t['fix_attempted']}'. Outcome: {t['outcome']}. Customer sentiment was {t['sentiment']}."
                print(f"Retaining ticket for {bank_id}...")
                client.retain(bank_id=bank_id, content=ticket_fact)
        except Exception as e:
            print(f"Failed to retain memory for {bank_id}: {e}")

    print("Memory seeding complete.")

if __name__ == "__main__":
    seed_hindsight()
