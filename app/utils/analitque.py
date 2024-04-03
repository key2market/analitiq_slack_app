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

def create_user(username, email):
    payload = {
        'username': username,
        'email': email,
        'password': os.environ.get("SECRET_KEY")
    }
    try:
        response = requests.post(
            os.environ.get("ANALITIQ_URL") + "/auth/signup",
            headers={},
            data=payload,
        )
        if not response or response.status_code != 200:
            raise Exception(
                f"Failed to post chat, request body: {pretty_json(payload)} response status: {response.status_code} response data: {pretty_json(response.json())}"
            )
        return response.json().get("username", None)
    except Exception as e:
        Logger.error(f"Error posting request to analitique")
        Logger.error(pretty_json(e))
        return None

def create_chat_session(chat_name):
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': 'Bearer ' + os.environ.get("ANALITIQ_ACCESS_TOKEN")
    }
    try:
        response = requests.post(
            os.environ.get("ANALITIQ_URL") + "/chat_session/create?chat_name=" + chat_name,
            headers=headers,
            data={},
        )
        if not response or response.status_code != 200:
            raise Exception(
                f"Failed to post chat, response status: {response.status_code} response data: {pretty_json(response.json())}"
            )
        return response.json()
    except Exception as e:
        Logger.error(f"Error posting request to analitique")
        Logger.error(pretty_json(e))
        return None
    
def get_chat_session(chat_name):
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': 'Bearer ' + os.environ.get("ANALITIQ_ACCESS_TOKEN")
    }
    try:
        response = requests.get(
            os.environ.get("ANALITIQ_URL") + "/chat_session/chat_name/" + chat_name,
            headers=headers,
            data={},
        )
        if not response or response.status_code != 200:
            raise Exception(
                f"Failed to post chat, response status: {response.status_code} response data: {pretty_json(response.json())}"
            )
        return response.json()
    except Exception as e:
        Logger.error(f"Error posting request to analitique")
        Logger.error(pretty_json(e))
        return None

def post_query(chat_session_id, query):
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': 'Bearer ' + os.environ.get("ANALITIQ_ACCESS_TOKEN")
    }
    try:
        response = requests.post(
            os.environ.get("ANALITIQ_URL") + "/" + chat_session_id + "/query",
            headers=headers,
            data={'user_query': query},
        )
        if not response or response.status_code != 200:
            raise Exception(
                f"Failed to post chat, response status: {response.status_code} response data: {pretty_json(response.json())}"
            )
        return response.json()
    except Exception as e:
        Logger.error(f"Error posting request to analitique")
        Logger.error(pretty_json(e))
        return None