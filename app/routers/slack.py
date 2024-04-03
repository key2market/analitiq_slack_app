import hashlib
import hmac
import json
import os
from app.utils.analitque import create_chat_session, create_user, get_chat_session, post_query
from app.utils.slack_api import post_message
from fastapi import APIRouter, Header, HTTPException, BackgroundTasks, Request
from typing import List, Optional
from pydantic import BaseModel, Field

router = APIRouter()

class SlackEvent(BaseModel):
    token: str
    challenge: Optional[str] = Field(None)
    type: str
    team_id: Optional[str]
    context_team_id: Optional[str]
    context_enterprise_id: Optional[str]
    api_app_id: Optional[str]
    event: Optional[dict]
    event_id: Optional[str]
    event_time: Optional[int]
    authorizations: Optional[List[dict]]
    is_ext_shared_channel: Optional[bool]
    event_context: Optional[str]

@router.get("/health")
async def handle_health():
    return "OK"

@router.post("/event")
async def slack_events(request: Request, background_tasks: BackgroundTasks):
    try:
        await verify_signature(request)
        # Retrieve the raw request body
        raw_body = await request.body()

        # Parse the JSON data from the request body
        body_data = json.loads(raw_body)
        # handle url verification
        if body_data["type"] == "url_verification":
            return {"challenge": body_data["challenge"]}
        # handle event callback
        elif body_data["type"] == "event_callback":
            # Check if the event is a message event
            if body_data["event"]["type"] == "message":
                # Check if the message is not from a bot
                if "bot_id" not in body_data["event"]:
                    # Enqueue processing of message in background
                    background_tasks.add_task(process_message, body_data["event"])
                    return {"message": "Processing message in background"}
    except HTTPException as e:
        print(e)
        return e

async def verify_signature(request: Request):
    slack_signature = request.headers.get("X-Slack-Signature")
    slack_timestamp = request.headers.get("X-Slack-Request-Timestamp")

    if not slack_signature or not slack_timestamp:
        raise HTTPException(status_code=400, detail="Slack signature headers not provided")

    # Retrieve the raw request body
    request_body = await request.body()

    base_string = f'v0:{slack_timestamp}:{request_body.decode("utf-8")}'.encode('utf-8')
    # Calculate the expected signature
    expected_signature = 'v0=' + hmac.new(os.getenv('SLACK_SIGNING_SECRET').encode('utf-8'), base_string, hashlib.sha256).hexdigest()

    # Compare the signatures
    if not hmac.compare_digest(expected_signature, slack_signature):
        print("Invalid Slack signature")
        raise HTTPException(status_code=403, detail="Invalid Slack signature")


def process_message(event: dict):
    # Implement your message processing logic here
    print("Message from user")
    print(event)
    chat_sessions = get_chat_session(chat_name=event["user"])
    # Check that chat_sessions is not None and not an empty list
    if not chat_sessions:
        chat_sessions = create_chat_session(chat_name=event["user"])
        chat_sessions = get_chat_session(chat_name=event["user"])
    if not chat_sessions:
        raise HTTPException(status_code=500, detail="Failed to create chat session")
    chat_session = chat_sessions[0]
    response_to_query = post_query(chat_session_id=chat_session["id"], query=event["text"])
    if not response_to_query:
        raise HTTPException(status_code=500, detail="Failed to post query")
    post_message(bot_token=os.getenv('SLACK_BOT_OAUTH_TOKEN'), sink=event["user"], text=response_to_query["text"])