# Stage 1: Build with uv
FROM ghcr.io/astral-sh/uv:python3.10-alpine AS uv

# Set working directory
WORKDIR /app

# Enable bytecode compilation & copy mode
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Lock dependencies
RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv lock

# Sync dependencies (excluding project files for now)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen --no-install-project --no-dev --no-editable

# Add rest of the project and sync again (installs project itself)
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen --no-dev --no-editable

# Clean up
RUN find /app/.venv -name '__pycache__' -type d -exec rm -rf {} + && \
    find /app/.venv -name '*.pyc' -delete && \
    find /app/.venv -name '*.pyo' -delete

# Stage 2: Minimal final image
FROM python:3.10-alpine

# Create app user
RUN adduser -D -h /home/app -s /bin/sh app
WORKDIR /app
USER app

# Copy virtual environment
COPY --from=uv --chown=app:app /app/.venv /app/.venv
COPY --from=uv --chown=app:app /app /app

# Export the venv's bin to the PATH
ENV PATH="/app/.venv/bin:$PATH"

# Run with uvicorn
CMD ["uvicorn", "mcp_tekmetric.servers.main:asgi_app", "--host", "0.0.0.0", "--port", "8080"]
