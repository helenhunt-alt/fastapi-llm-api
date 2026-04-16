from typing import Any

import httpx

from app.core.config import settings
from app.core.errors import ExternalServiceError


class OpenRouterClient:
    def __init__(self) -> None:
        self._base_url = settings.openrouter_base_url.rstrip("/")
        self._api_key = settings.openrouter_api_key
        self._model = settings.openrouter_model
        self._site_url = settings.openrouter_site_url
        self._app_name = settings.openrouter_app_name

    async def get_chat_completion(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
    ) -> str:
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "HTTP-Referer": self._site_url,
            "X-Title": self._app_name,
            "Content-Type": "application/json",
        }

        payload = {
            "model": self._model,
            "messages": messages,
            "temperature": temperature,
        }

        url = f"{self._base_url}/chat/completions"

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, headers=headers, json=payload)
        except httpx.HTTPError as error:
            raise ExternalServiceError("Failed to connect to OpenRouter") from error

        if response.status_code >= 400:
            error_message = self._extract_error_message(response)
            raise ExternalServiceError(f"OpenRouter error: {error_message}")

        data = response.json()
        return self._extract_answer(data)

    @staticmethod
    def _extract_error_message(response: httpx.Response) -> str:
        try:
            data = response.json()
        except ValueError:
            return response.text or f"HTTP {response.status_code}"

        error = data.get("error")
        if isinstance(error, dict):
            message = error.get("message")
            if isinstance(message, str) and message.strip():
                return message

        return response.text or f"HTTP {response.status_code}"

    @staticmethod
    def _extract_answer(data: dict[str, Any]) -> str:
        choices = data.get("choices")
        if not isinstance(choices, list) or not choices:
            raise ExternalServiceError("OpenRouter returned an invalid response")

        first_choice = choices[0]
        if not isinstance(first_choice, dict):
            raise ExternalServiceError("OpenRouter returned an invalid response")

        message = first_choice.get("message")
        if not isinstance(message, dict):
            raise ExternalServiceError("OpenRouter returned an invalid response")

        content = message.get("content")
        if isinstance(content, str) and content.strip():
            return content

        raise ExternalServiceError("OpenRouter returned an empty answer")