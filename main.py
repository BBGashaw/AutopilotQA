from fastapi import FastAPI, Request, Header, HTTPException
import hmac
import hashlib
import json

app = FastAPI()

# Your secret from GitHub webhook settings — keep this safe!
GITHUB_SECRET = "your_webhook_secret_here"

def verify_github_signature(signature: str, body: bytes) -> bool:
    sha_name, signature = signature.split('=')
    if sha_name != 'sha256':
        return False
    mac = hmac.new(GITHUB_SECRET.encode(), msg=body, digestmod=hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), signature)

@app.post("/webhook")
async def github_webhook(request: Request, x_hub_signature_256: str = Header(None), x_github_event: str = Header(None)):
    body = await request.body()

    # Verify signature
    if x_hub_signature_256 is None or not verify_github_signature(x_hub_signature_256, body):
        raise HTTPException(status_code=403, detail="Invalid signature")

    payload = await request.json()

    # We only care about pull_request events for MVP
    if x_github_event != "pull_request":
        return {"message": "Event ignored"}

    action = payload.get("action")
    if action not in ["opened", "synchronize", "reopened"]:
        return {"message": f"Ignored pull request action: {action}"}

    # Extract PR info
    pr_number = payload["number"]
    pr_title = payload["pull_request"]["title"]
    pr_diff_url = payload["pull_request"]["diff_url"]

    # For now, just log these and respond
    print(f"PR #{pr_number} '{pr_title}' - diff URL: {pr_diff_url}")

    # Next step will be to fetch diff and process it

    return {"message": f"Received PR #{pr_number} event: {action}"}
