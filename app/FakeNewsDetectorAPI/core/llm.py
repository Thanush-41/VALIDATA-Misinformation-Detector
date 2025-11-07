import logging
from typing import Tuple, Optional
import os

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


def query_openai(prompt: str) -> Tuple[bool, str]:
    """Send a prompt to OpenAI and return a tuple(success flag, message)."""
    try:
        import openai
    except ImportError:
        return False, "OpenAI package not installed. Run: pip install openai"
    
    api_key = getattr(settings, 'OPENAI_API_KEY', None)
    if not api_key:
        return False, "OPENAI_API_KEY not configured in settings"
    
    model = getattr(settings, 'OPENAI_MODEL', 'gpt-3.5-turbo')
    
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a news analyst. Provide concise, factual analysis."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7,
        )
        content = response.choices[0].message.content
        return True, content.strip()
    except Exception as exc:
        logger.exception('Failed to query OpenAI.')
        return False, f'OpenAI request failed: {exc}'


def query_anthropic(prompt: str) -> Tuple[bool, str]:
    """Send a prompt to Anthropic Claude and return a tuple(success flag, message)."""
    try:
        import anthropic
    except ImportError:
        return False, "Anthropic package not installed. Run: pip install anthropic"
    
    api_key = getattr(settings, 'ANTHROPIC_API_KEY', None)
    if not api_key:
        return False, "ANTHROPIC_API_KEY not configured in settings"
    
    model = getattr(settings, 'ANTHROPIC_MODEL', 'claude-3-haiku-20240307')
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model=model,
            max_tokens=500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        content = message.content[0].text
        return True, content.strip()
    except Exception as exc:
        logger.exception('Failed to query Anthropic.')
        return False, f'Anthropic request failed: {exc}'


def query_huggingface(prompt: str) -> Tuple[bool, str]:
    """Send a prompt to Hugging Face Inference API and return a tuple(success flag, message)."""
    api_key = getattr(settings, 'HUGGINGFACE_API_KEY', None)
    if not api_key:
        return False, "HUGGINGFACE_API_KEY not configured in settings"
    
    model = getattr(settings, 'HUGGINGFACE_MODEL', 'mistralai/Mistral-7B-Instruct-v0.2')
    url = f"https://api-inference.huggingface.co/models/{model}"
    
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.7,
            "return_full_text": False
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            content = data[0].get('generated_text', '')
            return True, content.strip()
        else:
            return False, f'Unexpected Hugging Face response format: {data}'
    except Exception as exc:
        logger.exception('Failed to query Hugging Face.')
        return False, f'Hugging Face request failed: {exc}'


def query_google(prompt: str) -> Tuple[bool, str]:
    """Send a prompt to Google Gemini and return a tuple(success flag, message)."""
    try:
        import google.generativeai as genai
    except ImportError:
        return False, "google-generativeai package not installed. Run: pip install google-generativeai"
    
    api_key = getattr(settings, 'GOOGLE_API_KEY', None)
    if not api_key:
        return False, "GOOGLE_API_KEY not configured in settings"
    
    model_name = getattr(settings, 'GOOGLE_MODEL', 'gemini-pro')
    
    try:
        genai.configure(api_key=api_key)
        # Use the correct model name - try gemini-1.5-flash-latest or gemini-pro
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        return True, response.text.strip()
    except Exception as exc:
        logger.exception('Failed to query Google Gemini.')
        return False, f'Google Gemini request failed: {exc}'


def query_llm(prompt: str, provider: Optional[str] = None) -> Tuple[bool, str]:
    """
    Universal LLM query function that routes to the configured provider.
    
    Args:
        prompt: The prompt to send to the LLM
        provider: Override the default provider (ollama, openai, anthropic, huggingface, none)
    
    Returns:
        Tuple of (success: bool, response: str)
    """
    if provider is None:
        provider = getattr(settings, 'LLM_PROVIDER', 'ollama').lower()
    
    logger.info(f'Querying LLM with provider: {provider}')
    
    if provider == 'ollama':
        return query_ollama(prompt)
    elif provider == 'openai':
        return query_openai(prompt)
    elif provider == 'anthropic':
        return query_anthropic(prompt)
    elif provider == 'google':
        return query_google(prompt)
    elif provider == 'huggingface':
        return query_huggingface(prompt)
    elif provider == 'none':
        return False, "LLM analysis disabled"
    else:
        logger.warning(f'Unknown LLM provider: {provider}. Falling back to Ollama.')
        return query_ollama(prompt)
