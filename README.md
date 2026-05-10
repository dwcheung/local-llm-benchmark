# Local LLM Benchmark

A simple benchmarking tool for testing local LLM performance.

## LLM inference metrics
- **Time to First Token (TTFT)**: how long a user needs to wait before seeing the model’s output
- **Input Token Per Second (Input-TPS)**: total input tokens per seconds
- **Token Per Second (TPS)**: total output tokens per seconds
- **Inter-token Latency (ITL)**: the average time between consecutive tokens

The goal is to compare how different local LLMs perform on a set of prompts.
Note: Performance outcome varies depending on the hardware you are running it on, including CPU, RAM, system load.

## Ollama's API Usage
- `prompt_eval_count`: how many input tokens were processed
- `prompt_eval_duration`: how long it took to evaluate the prompt
- `eval_count`: how many output tokens were processes
- `eval_duration`: how long it took to generate the output tokens
