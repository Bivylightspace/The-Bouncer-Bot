# Bouncer Bot

A Slack bot to add or remove users from channels, built with Python and FastAPI.

## Features
- Invite users to channels
- Remove users from channels
- List all channels

## Setup

1. **Clone the repository**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up your `.env` file:**
   - `SLACK_BOT_TOKEN`: Your Slack bot token
   - (Optional) `APP_NAME`, `APP_VERSION`, `APP_DESCRIPTION`

4. **Run locally:**
   ```bash
   python main.py
   ```

## Deployment

This project is ready to deploy on [Vercel](https://vercel.com/) using the provided `vercel.json` configuration.

## Project Structure
```
bouncer/
├── bot/
│   ├── __init__.py
│   ├── core.py
│   └── config.py
├── main.py
├── requirements.txt
├── .env
├── vercel.json
```

## License
See [LICENSE](LICENSE) for details. 