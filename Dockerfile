FROM python:3.13-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync

COPY .env .env
COPY adapters adapters
COPY domain domain

EXPOSE 8000

CMD ["uv", "run", "-m", "domain.telegram_bot.bot"]
