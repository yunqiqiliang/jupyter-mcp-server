FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml pyproject.toml
COPY jupyter_mcp_server/* jupyter_mcp_server/

RUN pip install -e .

CMD ["python", "-m", "jupyter_mcp_server.server"]