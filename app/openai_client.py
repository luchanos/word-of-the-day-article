import httpx
from httpx import Response

OPENAI_API_KEY = "your_openai_api_key"


class AsyncOpenAIClient:
    def __init__(self, api_key: str, base_url: str = "api.openai.com"):
        self.api_key = api_key
        self.base_url = base_url

    def generate_headers(self):
        return {
        "Authorization": f"Bearer {self.api_key}",
        "Content-Type": "application/json"
    }

    async def make_prompt_request(
            self,
            prompt: str,
            max_tokens: int = 100,
            temperature: float = 0.5,
            n: int = 1,
            stop=None,
            model: str = "gpt-3.5-turbo",
    ) -> Response:
        headers = self.generate_headers()
        payload = {
            "model": model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "n": n,
            "stop": stop,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post("https://api.openai.com/v1/completions", json=payload, headers=headers)
            response.raise_for_status()
            return response
