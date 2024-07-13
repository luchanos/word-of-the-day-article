import httpx
from httpx import Response, HTTPStatusError, RequestError


class AsyncOpenAIClient:
    def __init__(self, api_key: str, base_url: str = "api.openai.com"):
        self.api_key = api_key
        self.base_url = base_url

    def generate_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    @staticmethod
    def build_payload(
            prompt: str,
            max_tokens: int = 100,
            temperature: float = 0.5,
            n: int = 1,
            stop=None,
            model: str = "gpt-3.5-turbo"
    ):
        return {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "n": n,
            "stop": stop
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
        payload = self.build_payload(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            n=n,
            stop=stop,
            model=model,
        )
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"https://{self.base_url}/v1/chat/completions", json=payload, headers=headers)
                response.raise_for_status()
                return response
        except HTTPStatusError as e:
            raise RuntimeError(f"HTTP error occurred: {e.response.status_code} {e.response.text}") from e
        except RequestError as e:
            raise RuntimeError(f"Request error occurred: {str(e)}") from e
