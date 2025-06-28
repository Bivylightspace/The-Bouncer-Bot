from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from bot.config import settings


class SlackService:
    @staticmethod
    def _client():
        return WebClient(token=settings.SLACK_BOT_TOKEN)

    @staticmethod
    def get_user_id_by_username(username: str) -> str:
        try:
            response = SlackService._client().users_list()
            for user in response["members"]:
                if user["name"] == username:
                    return user["id"]
            raise Exception(f"User with username '{username}' not found.")
        except SlackApiError as e:
            raise Exception(f"Could not find user: {e.response['error']}")

    @staticmethod
    def invite_users_to_channel(usernames: list, channel_id: str):
        results = []
        for username in usernames:
            try:
                user_id = SlackService.get_user_id_by_username(username)
                SlackService._client().conversations_invite(channel=channel_id, users=user_id)
                results.append(f"User {username} invited to {channel_id}")
            except Exception as e:
                results.append(f"Failed to invite {username}: {str(e)}")
        return results

    @staticmethod
    def remove_users_from_channel(usernames: list, channel_id: str):
        results = []
        for username in usernames:
            try:
                user_id = SlackService.get_user_id_by_username(username)
                SlackService._client().conversations_kick(channel=channel_id, user=user_id)
                results.append(f"User {username} removed from {channel_id}")
            except Exception as e:
                results.append(f"Failed to remove {username}: {str(e)}")
        return results

    @staticmethod
    def invite_user_ids_to_channel(user_ids: list, channel_id: str):
        results = []
        for user_id in user_ids:
            try:
                SlackService._client().conversations_invite(channel=channel_id, users=user_id)
                results.append(f"User {user_id} invited to {channel_id}")
            except Exception as e:
                results.append(f"Failed to invite {user_id}: {str(e)}")
        return results

    @staticmethod
    def remove_user_ids_from_channel(user_ids: list, channel_id: str):
        results = []
        for user_id in user_ids:
            try:
                SlackService._client().conversations_kick(channel=channel_id, user=user_id)
                results.append(f"User {user_id} removed from {channel_id}")
            except Exception as e:
                results.append(f"Failed to remove {user_id}: {str(e)}")
        return results

    @staticmethod
    def list_channels(channel_name=None):
        response = SlackService._client().conversations_list(
            types="public_channel,private_channel")
        channels = response["channels"]
        if channel_name:
            channels = [c for c in channels if c["name"] == channel_name]
        return [{"name": c["name"], "id": c["id"]} for c in channels]

    @staticmethod
    def list_channels_cli():
        channels = SlackService.list_channels()
        for channel in channels:
            print(f"{channel['name']} - {channel['id']}")

    @staticmethod
    def add_to_trenches(user_ids: list):
        trenches = SlackService.list_channels(settings.TRENCHES)
        if not trenches:
            return ["Trenches channel not found."]
        channel_id = trenches[0]["id"]
        return SlackService.invite_user_ids_to_channel(user_ids, channel_id)
