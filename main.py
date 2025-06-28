from fastapi import FastAPI, Request, status
from slack_sdk.signature import SignatureVerifier
from bot.config import settings
from bot.core import SlackService
from starlette.responses import JSONResponse
from urllib.parse import parse_qs
import re
import logging

logger = logging.getLogger("slack")
logging.basicConfig(level=logging.INFO)
app = FastAPI()
verifier = SignatureVerifier(signing_secret=settings.SLACK_SIGNING_SECRET)


def parse_slack_form(request: Request):
    async def inner():
        body = await request.body()
        form = parse_qs(body.decode())
        text = form.get("text", [""])[0]
        channel_id = form.get("channel_id", [""])[0]
        user_ids = re.findall(r"<@([A-Z0-9]+)(?:\|[^>]+)?>", text)

        if user_ids:
            return user_ids, channel_id, True

        raw_words = text.replace(',', ' ').split()
        usernames = [
            word.strip().lstrip('@').replace(" ", "").lower()
            for word in raw_words if word.strip()
        ]
        return usernames, channel_id, False
    return inner


@app.post("/slack/add_user")
async def add_user(request: Request):
    raw_body = await request.body()
    logger.info(f"Slack raw body: {raw_body.decode()}")

    ids_or_names, channel_id, is_user_id = await parse_slack_form(request)()
    if is_user_id:
        results = SlackService.invite_user_ids_to_channel(
            ids_or_names, channel_id)
    else:
        results = SlackService.invite_users_to_channel(
            ids_or_names, channel_id)

    return JSONResponse(content={"text": "\n".join(results)})


@app.post("/slack/remove_user")
async def remove_user(request: Request):
    raw_body = await request.body()
    logger.info(f"Slack raw body: {raw_body.decode()}")

    ids_or_names, channel_id, is_user_id = await parse_slack_form(request)()
    if is_user_id:
        results = SlackService.remove_user_ids_from_channel(
            ids_or_names, channel_id)
    else:
        results = SlackService.remove_users_from_channel(
            ids_or_names, channel_id)

    return JSONResponse(
        content={"text": "\n".join(results)},
        status_code=status.HTTP_200_OK
    )


@app.get("/slack/list_channels")
async def list_channels_endpoint():
    try:
        channels = SlackService.list_channels()
        return {"channels": channels}
    except Exception as e:
        return {"error": str(e)}


@app.post("/slack/add/trenchs")
async def add_to_trenches(request: Request):
    raw_body = await request.body()
    logger.info(f"Slack raw body: {raw_body.decode()}")

    ids_or_names, _, is_user_id = await parse_slack_form(request)()

    if is_user_id:
        results = SlackService.add_to_trenches(ids_or_names)
    else:
        user_ids = []
        for username in ids_or_names:
            try:
                user_id = SlackService.get_user_id_by_username(username)
                user_ids.append(user_id)
            except Exception as e:
                logger.error(
                    f"Failed to resolve username {username}: {str(e)}")
                user_ids.append(f"Failed to resolve {username}: {str(e)}")
        results = SlackService.add_to_trenches(user_ids)

    return JSONResponse(
        content={"text": "\n".join(results)},
        status_code=status.HTTP_200_OK
    )


@app.get("/")
async def home():
    return {
        "app_name": settings.APP_NAME,
        "app_version": settings.APP_VERSION,
        "app_description": settings.APP_DESCRIPTION,
        "message": "Hi from Ayobamidele Ewetuga."
    }


if __name__ == "__main__":
    SlackService.list_channels_cli()
