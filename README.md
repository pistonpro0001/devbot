# devbot

Discord bot for developer utilities.

## Requirements

- Python 3.11+
- A Discord bot token ([Discord Developer Portal](https://discord.com/developers/applications))

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DISCORD_API` | **Yes** | Discord bot token. Read at startup via `os.getenv("DISCORD_API")`. The process raises `ValueError` if it is missing or empty. |

Example:

```bash
export DISCORD_API="your-bot-token-here"
python devbot.py
```

Or a `.env` file loaded by your process manager / shell:

```bash
DISCORD_API=your-bot-token-here
```

Do not commit real tokens.

## Install

```bash
pip install -r requirements.txt
# or
uv sync
```

## License

See [LICENSE](LICENSE).
