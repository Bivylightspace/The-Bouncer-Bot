from fastapi import FastAPI, Request
from slack_sdk.signature import SignatureVerifier
from bot.config import settings
from bot.core import invite_users_to_channel, remove_users_from_channel, list_channels
from starlette.responses import JSONResponse
from urllib.parse import parse_qs
import re

import logging

logger = logging.getLogger("slack")
logging.basicConfig(level=logging.INFO)
app = FastAPI()
verifier = SignatureVerifier(signing_secret=getattr(settings, 'SLACK_SIGNING_SECRET', ''))

def parse_slack_form(request: Request):
    async def inner():
        body = await request.body()
        form = parse_qs(body.decode())
        text = form.get("text", [""])[0]
        channel_id = form.get("channel_id", [""])[0]
        # Extract user IDs from <@USERID> mentions
        user_ids = re.findall(r"<@([A-Z0-9]+)>", text)
        if user_ids:
            return user_ids, channel_id, True
        # Fall back to raw usernames
        raw_words = text.replace(',', ' ').split()
        usernames = [
            word.strip().lstrip('@').replace(" ", "").lower()
            for word in raw_words if word.strip()
        ]
        return usernames, channel_id, False
    return inner


@app.post("/slack/add_user")
async def add_user(request: Request):
    # 🔍 Log raw body
    raw_body = await request.body()
    logger.info(f"Slack raw body: {raw_body.decode()}")

    # 🔍 Parse and log structured form data
    form_data = parse_qs(raw_body.decode())
    logger.info(f"Slack parsed form: {form_data}")

    # ✅ Proceed with your logic
    ids_or_names, channel_id, is_user_id = await parse_slack_form(request)()
    if is_user_id:
        from bot.core import invite_user_ids_to_channel
        results = invite_user_ids_to_channel(ids_or_names, channel_id)
    else:
        results = invite_users_to_channel(ids_or_names, channel_id)

    return {"text": "\n".join(results)}


@app.post("/slack/remove_user")
async def remove_user(request: Request):
    ids_or_names, channel_id, is_user_id = await parse_slack_form(request)()
    if is_user_id:
        from bot.core import remove_user_ids_from_channel
        results = remove_user_ids_from_channel(ids_or_names, channel_id)
    else:
        results = remove_users_from_channel(ids_or_names, channel_id)
    return {"text": "\n".join(results)}

@app.get("/slack/list_channels")
async def list_channels_endpoint():
    try:
        channels = list_channels()
        return {"channels": channels}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
async def home():
    return {
        "app_name": settings.APP_NAME,
        "app_version": settings.APP_VERSION,
        "app_description": settings.APP_DESCRIPTION,
        "message": "Hi from Ayobamidele Ewetuga."
    }

if __name__ == "__main__":
    from bot.core import list_channels_cli
    list_channels_cli()
