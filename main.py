from fastapi import FastAPI, Request, Form
from slack_sdk.signature import SignatureVerifier
from bot.config import settings
from bot.core import get_user_id_by_email, invite_user_to_channel, remove_user_from_channel
from bot.core import list_channels

app = FastAPI()

verifier = SignatureVerifier(signing_secret=settings.SLACK_SIGNING_SECRET)

@app.post("/slack/add_user")
async def add_user(request: Request, text: str = Form(...), channel_id: str = Form(...)):
    if not verifier.is_valid_request(await request.body(), request.headers):
        return {"text": "Invalid request signature"}

    email = text.strip()
    try:
        user_id = get_user_id_by_email(email)
        result = invite_user_to_channel(user_id, channel_id)
        return {"text": result}
    except Exception as e:
        return {"text": f"Error: {str(e)}"}

@app.post("/slack/remove_user")
async def remove_user(request: Request, text: str = Form(...), channel_id: str = Form(...)):
    if not verifier.is_valid_request(await request.body(), request.headers):
        return {"text": "Invalid request signature"}

    email = text.strip()
    try:
        user_id = get_user_id_by_email(email)
        result = remove_user_from_channel(user_id, channel_id)
        return {"text": result}
    except Exception as e:
        return {"text": f"Error: {str(e)}"}

if __name__ == "__main__":
    list_channels()
