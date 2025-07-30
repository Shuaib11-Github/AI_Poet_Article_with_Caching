from __future__ import annotations

import json
import logging
from typing import Any, Dict, List

import requests
from requests import Response

from .config import get_settings
from .exceptions import APIError

log = logging.getLogger(__name__)


def _post(payload: Dict[str, Any]) -> Response:
    cfg = get_settings()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {cfg.api_key}",
    }

    log.debug("POST %s | payload=%s", cfg.base_url, payload)

    resp = requests.post(
        cfg.base_url, headers=headers, json=payload, timeout=30
    )
    if not resp.ok:
        raise APIError(resp.status_code, resp.text)
    return resp


def chat_completion(
    messages: List[Dict[str, str]],
    model: str | None = None,
    max_tokens: int | None = None,
    temperature: float | None = None,
) -> str:
    """
    Low-level wrapper → returns *assistant* message content text.
    """
    cfg = get_settings()

    payload = {
        "messages": messages,
        "model": model or cfg.default_model,
        "max_tokens": max_tokens or cfg.max_tokens,
        "temperature": temperature or cfg.temperature,
    }

    resp = _post(payload)
    data = resp.json()

    # Defensive parsing
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise APIError(
            resp.status_code, f"Unexpected response: {json.dumps(data)}"
        ) from exc