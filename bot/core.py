from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from bot.config import settings

client = WebClient(token=settings.SLACK_BOT_TOKEN)

def get_user_id_by_username(username: str) -> str:
    try:
        response = client.users_list()
        for user in response["members"]:
            if user["name"] == username:
                return user["id"]
        raise Exception(f"User with username '{username}' not found.")
    except SlackApiError as e:
        raise Exception(f"Could not find user: {e.response['error']}")

def invite_users_to_channel(usernames: list, channel_id: str):
    results = []
    for username in usernames:
        try:
            user_id = get_user_id_by_username(username)
            client.conversations_invite(channel=channel_id, users=user_id)
            results.append(f"User {username} invited to {channel_id}")
        except Exception as e:
            results.append(f"Failed to invite {username}: {str(e)}")
    return results

def remove_user_from_channel(user_id: str, channel_id: str):
    try:
        client.conversations_kick(channel=channel_id, user=user_id)
        return f"User {user_id} removed from {channel_id}"
    except SlackApiError as e:
        raise Exception(f"Remove failed: {e.response['error']}")

def remove_users_from_channel(usernames: list, channel_id: str):
    results = []
    for username in usernames:
        try:
            user_id = get_user_id_by_username(username)
            client.conversations_kick(channel=channel_id, user=user_id)
            results.append(f"User {username} removed from {channel_id}")
        except Exception as e:
            results.append(f"Failed to remove {username}: {str(e)}")
    return results

def list_channels():
    response = client.conversations_list(types="public_channel,private_channel")
    return [{"name": channel["name"], "id": channel["id"]} for channel in response["channels"]]

def list_channels_cli():
    channels = list_channels()
    for channel in channels:
        print(f"{channel['name']} - {channel['id']}")

def invite_user_ids_to_channel(user_ids: list, channel_id: str):
    results = []
    for user_id in user_ids:
        try:
            client.conversations_invite(channel=channel_id, users=user_id)
            results.append(f"User {user_id} invited to {channel_id}")
        except Exception as e:
            results.append(f"Failed to invite {user_id}: {str(e)}")
    return results

def remove_user_ids_from_channel(user_ids: list, channel_id: str):
    results = []
    for user_id in user_ids:
        try:
            client.conversations_kick(channel=channel_id, user=user_id)
            results.append(f"User {user_id} removed from {channel_id}")
        except Exception as e:
            results.append(f"Failed to remove {user_id}: {str(e)}")
    return results 