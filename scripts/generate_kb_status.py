import json

def generate_kb_and_status():
    kb_articles = [
        {"id": "kb_1", "title": "Invoice Sync Failures", "content": "If invoice sync fails, first try reconnecting the integration. If it fails again, try clearing the cache. If both fail, escalate to tier 2 for manual DB sync."},
        {"id": "kb_2", "title": "Duplicate Charges", "content": "Duplicate charges occur when the payment gateway sends two webhooks. Refund the duplicate via Stripe dashboard."},
        {"id": "kb_3", "title": "Tax Settings Incorrect", "content": "Ensure regional tax compliance is enabled in Settings > Tax. Manual override is needed for EU VAT."},
        {"id": "kb_4", "title": "Login/SSO Issues", "content": "SSO failures are usually due to expired SAML certificates. Request a new cert from the IT admin."},
        {"id": "kb_5", "title": "API Rate Limits", "content": "Standard rate limit is 100 req/min. Can be temporarily increased for Enterprise customers upon request."},
        {"id": "kb_6", "title": "Export Errors (CSV)", "content": "CSV exports fail if data contains unescaped commas. Recommend using JSON export as a workaround."},
        {"id": "kb_7", "title": "Refund Processing Error", "content": "Refunds may fail if the original charge is older than 90 days. Require manual wire transfer."},
        {"id": "kb_8", "title": "QuickBooks Specific Sync", "content": "QuickBooks requires matching chart of accounts. Sync will fail if an account is deleted in QB."}
    ]

    mock_invoices = [
        {"id": "INV-1001", "customer_id": "hero_priya", "status": "failed_sync", "amount": 1500.00, "date": "10 days ago"},
        {"id": "INV-1002", "customer_id": "hero_priya", "status": "failed_sync", "amount": 1500.00, "date": "2 days ago"},
        {"id": "INV-1003", "customer_id": "cust_01", "status": "paid", "amount": 5000.00, "date": "15 days ago"}
    ]

    status_page = {
        "active_incident": True,
        "incident_title": "Intermittent sync delays with QuickBooks",
        "severity": "minor",
        "description": "We are currently seeing intermittent delays when syncing invoices to QuickBooks Online. Reconnecting the integration does not resolve this. Engineering is investigating."
    }

    with open("../data/kb_articles.json", "w") as f:
        json.dump(kb_articles, f, indent=2)
    
    with open("../data/mock_db.json", "w") as f:
        json.dump({"invoices": mock_invoices, "status_page": status_page}, f, indent=2)

if __name__ == "__main__":
    generate_kb_and_status()
