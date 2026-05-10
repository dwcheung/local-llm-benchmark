import json
import requests


class OllamaClient:
    def __init__(self, url="http://localhost:11434/api/generate"):
        self.url = url

    def generate(self, model, prompt):
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": True,
        }

        output = requests.post(self.url, json=payload, stream=True)
        output.raise_for_status()

        for line in output.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                chunk = json.loads(decoded_line)
                yield chunk