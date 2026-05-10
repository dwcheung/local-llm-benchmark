from src.ollama_client import OllamaClient
from src.benchmark import Benchmark
from src.report import print_result, save_results_csv, save_summary_csv


MODELS = [
    "qwen2.5:1.5b",
    "llama3.2:1b",
    "deepseek-r1:1.5b",
]


def load_prompts(filename):
    prompts = []

    file = open(filename, "r", encoding="utf-8")

    for line in file:
        prompt = line.strip()
        if prompt != "":
            prompts.append(prompt)

    file.close()

    return prompts


def main():
    prompts = load_prompts("prompts/basic_prompts.txt")

    client = OllamaClient()
    benchmark = Benchmark(client)

    results = []

    for model in MODELS:
        for prompt in prompts:
            result = benchmark.run(model, prompt)
            results.append(result)
            print_result(result)

    save_results_csv(results, "results/benchmark_results.csv")
    save_summary_csv(results, "results/summary_results.csv")


if __name__ == "__main__":
    main()