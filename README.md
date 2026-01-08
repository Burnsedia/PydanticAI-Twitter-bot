# PydanticAI Twitter Bot

An autonomous Twitter bot that researches Hacker News and Twitter trends to generate viral tweets (targeting 10k+ engagements) in a specific style, using PydanticAI agents.

## Features

- **Research Agent**: Fetches HN top stories and Twitter trends, identifies viral topics.
- **Opinion Agent**: Derives opinions from your blog and GitHub projects.
- **Tweet Agent**: Generates engaging tweets or threads.
- **Posting Agent**: Posts to Twitter with thread support.
- **Extensible Sources**: Dependency injection for HN, Twitter, RSS feeds.
- **Data Persistence**: SQLAlchemy with Pydantic models.

## Setup

1. Clone and install: `pip install -e .[dev]`
2. Copy `.env.example` to `.env` and fill in credentials.
3. Run migrations: `alembic upgrade head`
4. Run the bot: `python -m src.main`

## Development

- Build components in `src/`: Start with models, then sources, agents.
- Test with pytest.
- Add new sources via DI in `src/di.py`.

## Architecture

See `src/` for modular code: models, sources, agents, services.

For details, see the project plan.