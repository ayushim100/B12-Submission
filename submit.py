import json
import hmac
import hashlib
import requests
import os
from datetime import datetime, timezone

# ==== CONFIG ====
SIGNING_SECRET = b"hello-there-from-b12"
URL = "https://b12.io/apply/submission"

payload = {
    "action_run_link": "https://github.com/YOUR_USERNAME/YOUR_REPO/actions/runs/YOUR_RUN_ID",
    "email": "you@example.com",
    "name": "Your name",
    "repository_link": "https://github.com/YOUR_USERNAME/YOUR_REPO",
    "resume_link": "https://your-resume-link.com",
    "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
}

repo = os.getenv("GITHUB_REPOSITORY")
run_id = os.getenv("GITHUB_RUN_ID")

payload["action_run_link"] = f"https://github.com/{repo}/actions/runs/{run_id}"

# ==== CANONICAL JSON ====
body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")

# ==== SIGNATURE ====
signature = hmac.new(SIGNING_SECRET, body, hashlib.sha256).hexdigest()
headers = {
    "Content-Type": "application/json",
    "X-Signature-256": f"sha256={signature}",
}

# ==== POST REQUEST ====
response = requests.post(URL, headers=headers, data=body)

# ==== HANDLE RESPONSE ====
if response.status_code == 200:
    data = response.json()
    print("Receipt:", data.get("receipt"))
else:
    print("Error:", response.status_code, response.text)
    exit(1)