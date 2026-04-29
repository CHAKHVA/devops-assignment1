"""FastAPI demo app for the DevOps CI/CD assignment.

Exposes three endpoints used to demonstrate the deployment pipeline and
to make blue/green promotions and rollbacks visually obvious:

- ``GET /``        : minimal HTML page with a version banner
- ``GET /health``  : liveness probe used by smoke tests
- ``GET /version`` : reports the running git commit (set by Render)
"""

import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

APP_NAME = "DevOps Assignment 1 - CI/CD Demo"

# Render injects the deployed commit SHA via RENDER_GIT_COMMIT.
# Locally and in tests we fall back to "dev" so the app still works.
APP_VERSION = (os.getenv("RENDER_GIT_COMMIT") or "dev")[:7]

# The "color" lets us distinguish the blue (prod) and green (staging)
# services in screenshots without needing two codebases.
APP_COLOR = os.getenv("APP_COLOR", "blue").lower()

app = FastAPI(title=APP_NAME)


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    banner_color = "#1f6feb" if APP_COLOR == "blue" else "#2ea043"
    return f"""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <title>{APP_NAME}</title>
        <style>
          body {{
            font-family: -apple-system, system-ui, sans-serif;
            max-width: 720px;
            margin: 40px auto;
            padding: 0 16px;
            color: #1f2328;
          }}
          .banner {{
            background: {banner_color};
            color: white;
            padding: 16px 20px;
            border-radius: 8px;
          }}
          code {{
            padding: 2px 6px;
          }}
          ul {{ line-height: 1.8; }}
        </style>
      </head>
      <body>
        <div class="banner">
          <h1 style="margin:0">{APP_NAME}</h1>
          <p style="margin:4px 0 0">
            environment: <strong>{APP_COLOR}</strong>
            &nbsp;&middot;&nbsp;
            version: <code>{APP_VERSION}</code>
          </p>
        </div>
        <h2>Endpoints</h2>
        <ul>
          <li><a href="/health">/health</a> &mdash; liveness probe</li>
          <li><a href="/version">/version</a> &mdash; running commit SHA</li>
          <li><a href="/docs">/docs</a> &mdash; OpenAPI UI</li>
        </ul>
      </body>
    </html>
    """


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/version")
def version() -> dict[str, str]:
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "color": APP_COLOR,
    }
