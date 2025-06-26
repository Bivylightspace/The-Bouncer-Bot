from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from bot.config import settings

client = WebClient(token=settings.SLACK_BOT_TOKEN)

def get_user_id_by_email(email: str) -> str:
    try:
        response = client.users_lookupByEmail(email=email)
        return response["user"]["id"]
    except SlackApiError as e:
        raise Exception(f"Could not find user: {e.response['error']}")

def invite_user_to_channel(user_id: str, channel_id: str):
    try:
        client.conversations_invite(channel=channel_id, users=user_id)
        return f"User {user_id} invited to {channel_id}"
    except SlackApiError as e:
        raise Exception(f"Invite failed: {e.response['error']}")

def remove_user_from_channel(user_id: str, channel_id: str):
    try:
        client.conversations_kick(channel=channel_id, user=user_id)
        return f"User {user_id} removed from {channel_id}"
    except SlackApiError as e:
        raise Exception(f"Remove failed: {e.response['error']}")

def list_channels():
    response = client.conversations_list()
    for channel in response["channels"]:
        print(f"{channel['name']} - {channel['id']}") 