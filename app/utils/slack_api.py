import os
from dotenv import load_dotenv

load_dotenv()

import json
import requests

class Logger:
    @staticmethod
    def error(message):
        print(f"ERROR: {message}")

def pretty_json(data):
    return json.dumps(data, indent=2)

def post_message(bot_token, sink, text, ts=None, blocks=None, metadata=None):
    print("Posting message to Slack")
    body = {
        "channel": sink,
        "text": text,
        "metadata": metadata,
    }
    if ts:
        body["thread_ts"] = ts
    if blocks:
        body["blocks"] = blocks
    try:
        response = requests.post(
            "https://slack.com/api/chat.postMessage",
            json=body,
            headers={
                "Authorization": f"Bearer {bot_token}"
            }
        )
        if not response or response.status_code != 200 or not response.json().get("ok"):
            raise Exception(
                f"Failed to post chat, request body: {pretty_json(body)} response status: {response.status_code} response data: {pretty_json(response.json())}"
            )
        return response.json().get("message", None)
    except Exception as e:
        Logger.error(f"Error posting message to {sink}")
        Logger.error(pretty_json(e))
        return None
