FROM sinapsis:base
COPY . /app

WORKDIR /app/.venv
RUN uv sync --frozen
RUN uv pip install sinapsis-langchain-readers[all] --extra-index-url https://pypi.sinapsis.tech