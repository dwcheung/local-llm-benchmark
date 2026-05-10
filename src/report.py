import csv


def print_result(result):
    print("-" * 80)
    print(f"Model: {result['model']}")
    print(f"Prompt: {result['prompt']}")
    print(f"Elapsed Time: {result['elapsed']:.2f} seconds")
    print(f"Time To First Token: {result['time_to_first_token']:.2f} seconds")
    print(f"Prompt Tokens: {result['prompt_eval_count']}")
    print(f"Prompt Tokens Per Second: {result['prompt_tokens_per_second']:.2f} tokens/sec")
    print(f"Output Tokens: {result['eval_count']}")
    print(f"Output Tokens Per Second: {result['tokens_per_second']:.2f} tokens/sec")
    print(f"Average Intertoken Latency: {result['average_intertoken_latency']:.4f} seconds")
    print()
    print("Output:")
    print(result["output"])
    print()


def save_results_csv(results, filename):
    if not results:
        return

    file = open(filename, "w", newline="", encoding="utf-8")

    column_names = results[0].keys()
    writer = csv.DictWriter(file, fieldnames=column_names)
    writer.writeheader()
    for result in results:
        writer.writerow(result)

    file.close()


def save_summary_csv(results, filename):
    if not results:
        return

    model_results = {}

    for result in results:
        model = result["model"]

        if model not in model_results:
            model_results[model] = []

        model_results[model].append(result)

    summaries = []

    for model in model_results:
        count = len(model_results[model])
        total_elapsed_time = 0
        total_time_to_first_token = 0
        total_prompt_tokens = 0
        total_prompt_tps = 0
        total_output_tokens = 0
        total_output_tps = 0
        total_intertoken_latency = 0

        for result in model_results[model]:
            total_elapsed_time += result["elapsed"]
            total_time_to_first_token += result["time_to_first_token"]
            total_prompt_tokens += result["prompt_eval_count"]
            total_prompt_tps += result["prompt_tokens_per_second"]
            total_output_tokens += result["eval_count"]
            total_output_tps += result["tokens_per_second"]
            total_intertoken_latency += result["average_intertoken_latency"]

        summary = {
            "model": model,
            "prompts_tested": count,
            "average_elapsed_time": total_elapsed_time / count,
            "average_time_to_first_token": total_time_to_first_token / count,
            "total_prompt_tokens": total_prompt_tokens,
            "average_prompt_tps": total_prompt_tps / count,
            "total_output_tokens": total_output_tokens,
            "average_output_tps": total_output_tps / count,
            "average_intertoken_latency": total_intertoken_latency / count,
        }

        summaries.append(summary)

    file = open(filename, "w", newline="", encoding="utf-8")

    column_names = summaries[0].keys()
    writer = csv.DictWriter(file, fieldnames=column_names)
    writer.writeheader()
    for summary in summaries:
        writer.writerow(summary)

    file.close()