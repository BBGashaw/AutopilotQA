from fastapi import FastAPI, Request, Header, HTTPException

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from AutopilotQA!"}

@app.post("/webhook")
async def github_webhook(request: Request, x_github_event: str = Header(None)):
    if x_github_event != "pull_request":
        return {"message": f"Ignored event type: {x_github_event}"}

    payload = await request.json()
    
    # Extract some info about the PR for now
    action = payload.get("action")
    pr_number = payload.get("number")
    pr_title = payload.get("pull_request", {}).get("title")
    
    print(f"Received PR event: action={action}, number={pr_number}, title={pr_title}")
    
    # For now just acknowledge receipt
    return {"message": f"Received PR event: {action} for PR #{pr_number}"}
