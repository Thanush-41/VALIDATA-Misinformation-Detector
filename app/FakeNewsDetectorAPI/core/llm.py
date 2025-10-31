import logging
from typing import Tuple

import requests
from django.conf import settings


logger = logging.getLogger(__name__)


def query_ollama(prompt: str) -> Tuple[bool, str]:
    """Send a prompt to Ollama and return a tuple(success flag, message)."""
    base_url = settings.OLLAMA_BASE_URL.rstrip('/')
    url = f"{base_url}/api/generate"
    payload = {
        'model': settings.OLLAMA_MODEL,
        'prompt': prompt,
        'stream': False,
    }

    try:
        response = requests.post(url, json=payload, timeout=settings.OLLAMA_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.exception('Failed to reach Ollama.')
        return False, f'Ollama request failed: {exc}'

    try:
        data = response.json()
    except ValueError as exc:
        logger.exception('Invalid JSON received from Ollama.')
        return False, f'Unable to parse Ollama response: {exc}'

    content = data.get('response')
    if not content:
        logger.warning('Ollama response missing "response" field: %s', data)
        return False, 'Ollama returned an empty response.'

    return True, content.strip()
