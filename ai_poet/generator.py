# ai_poet/generator.py   (full, minimal version)
import logging
from typing import Dict

from .cache import Cache
from .client import chat_completion
from .prompts import POEM_PROMPT
from .prompts import ARTICLE_PROMPT

log = logging.getLogger(__name__)
_cache = Cache()

def _normalize_topic(topic: str) -> str:
    return " ".join(topic.strip().lower().split()) 

def generate_poem(
    topic: str = "artificial intelligence",
    *,
    use_cache: bool = True,               # <- MUST be here
) -> str:
    norm_topic = _normalize_topic(topic)
    prompt = POEM_PROMPT.format(topic=norm_topic)

    if use_cache:
        cached = _cache.get(prompt)
        if cached:
            return cached

    messages: list[Dict[str, str]] = [{"role": "user", "content": prompt}]
    response = chat_completion(messages)

    if use_cache:
        _cache.set(prompt, response)

    return response

def generate_article(
    topic: str = "artificial intelligence",
    *,
    use_cache: bool = True,
) -> str:
    norm_topic = _normalize_topic(topic)    
    prompt = ARTICLE_PROMPT.format(topic=norm_topic)

    if use_cache:
        cached = _cache.get(prompt)
        if cached:
            return cached
    
    messages: list[Dict[str, str]] = [{"role": "user", "content": prompt}]
    response = chat_completion(messages)

    if use_cache:
        _cache.set(prompt, response)

    return response