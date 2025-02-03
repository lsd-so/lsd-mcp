# Generated by https://smithery.ai. See: https://smithery.ai/docs/config#dockerfile
# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS uv

# Install the project into /app
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy the necessary project files
COPY . .

# Install the project's dependencies using uv
RUN --mount=type=cache,target=/root/.cache/uv     --mount=type=bind,source=uv.lock,target=uv.lock     --mount=type=bind,source=pyproject.toml,target=pyproject.toml     uv sync --frozen --no-install-project --no-dev --no-editable

# Set environment variables for LSD
ENV LSD_USER=<your_email_here>
ENV LSD_API_KEY=<api_key_from_your_profile_page>

# Entrypoint to run the MCP server
ENTRYPOINT ["uv", "run", "mcp", "install", "app.py"]
