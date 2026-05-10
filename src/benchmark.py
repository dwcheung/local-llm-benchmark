import time


class Benchmark:
    def __init__(self, client):
        self.client = client

    def run(self, model, prompt) -> dict:
        start = time.time()

        output_parts = []
        first_token_time = None
        previous_token_time = None
        intertoken_latencies = []
        final_data = {}

        for chunk in self.client.generate(model, prompt):
            now = time.time()

            token_text = chunk.get("response", "")
            if token_text:
                output_parts.append(token_text)
                if first_token_time is None:
                    first_token_time = now
                if previous_token_time is not None:
                    intertoken_latencies.append(now - previous_token_time)
                previous_token_time = now

            if chunk.get("done"):
                final_data = chunk

        end = time.time()

        output = "".join(output_parts)
        elapsed = end - start

        if first_token_time is not None:
            time_to_first_token = first_token_time - start
        else:
            time_to_first_token = 0

        prompt_eval_count = final_data.get("prompt_eval_count", 0)
        prompt_eval_duration_sec = final_data.get("prompt_eval_duration", 0) / 10**9
        if prompt_eval_duration_sec > 0:
            prompt_tokens_per_second = prompt_eval_count / prompt_eval_duration_sec
        else:
            prompt_tokens_per_second = 0

        eval_count = final_data.get("eval_count", 0)
        eval_duration_sec = final_data.get("eval_duration", 0) / 10**9
        if eval_duration_sec > 0:
            tokens_per_second = eval_count / eval_duration_sec
        else:
            tokens_per_second = 0

        if len(intertoken_latencies) > 0:
            average_intertoken_latency = sum(intertoken_latencies) / len(intertoken_latencies)
        else:
            average_intertoken_latency = 0

        return {
            "model": model,
            "prompt": prompt,
            "output": output,
            "elapsed": elapsed,
            "time_to_first_token": time_to_first_token,
            "prompt_eval_count": prompt_eval_count,
            "prompt_tokens_per_second": prompt_tokens_per_second,
            "eval_count": eval_count,
            "tokens_per_second": tokens_per_second,
            "average_intertoken_latency": average_intertoken_latency,
        }