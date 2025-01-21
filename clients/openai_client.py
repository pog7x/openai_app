import httpx


class OpenAICLient:
    def __init__(self, api_key: str):
        self._api_key = api_key

    async def fetch_openai_response(self, prompt: str):
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self._api_key}", "Content-Type": "application/json"}
        transport = httpx.AsyncHTTPTransport(retries=1)

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 50,
        }

        async with httpx.AsyncClient(transport=transport, timeout=10) as client:
            response = await client.post(url, headers=headers, json=data)

            if response.status_code == httpx.codes.OK:
                response_data = response.json()
                generated_text = response_data["choices"][0]["message"]["content"]
                return generated_text
            else:
                raise Exception(f"Error: {response.status_code} - {response.text}")
