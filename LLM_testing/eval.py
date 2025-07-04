LANG_API = "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"
LANG_URL = "https://api.smith.langchain.com"
HUGGINGFACEHUB_API_TOKEN = "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"

import json
from huggingface_hub import InferenceClient
from langchain_community.llms import HuggingFaceHub
from langchain.evaluation import load_evaluator

# Define models to test
models = {
    "gpt2": "gpt2",
    "falcon-7b-instruct": "tiiuae/falcon-7b-instruct",
    "mistral-7b-instruct": "mistralai/Mistral-7B-Instruct-v0.1",
    "zephyr-7b-beta": "HuggingFaceH4/zephyr-7b-beta"
}

# Define prompts
prompts = [
    "What is the capital of France?",
    "Explain the concept of gravity in simple terms.",
    "Translate 'How are you?' into Spanish."
]

# Collect responses
all_responses = {}

for model_name, repo_id in models.items():
    print(f"[{model_name}] Using model: {repo_id}")
    client = InferenceClient(repo_id)

    model_responses = []
    for prompt in prompts:
        print(f"[{model_name}] Prompt: {prompt}")
        try:
            response = client.text_generation(prompt, max_new_tokens=100, temperature=0.7)
            print(f"→ Response:\n{response.strip()}\n")
            model_responses.append({"prompt": prompt, "response": response.strip()})
        except Exception as e:
            print(f"Error with model {model_name}: {e}")
            model_responses.append({"prompt": prompt, "response": f"[ERROR] {e}"})

    all_responses[model_name] = model_responses

# Save responses
with open("llm_outputs.json", "w", encoding="utf-8") as f:
    json.dump(all_responses, f, indent=2, ensure_ascii=False)

print("✅ Responses saved to llm_outputs.json")

# --- EVALUATION ---

# Use a Hugging Face model as evaluator
evaluator_llm = HuggingFaceHub(
    repo_id="mistralai/Mistral-7B-Instruct-v0.1",  
    model_kwargs={"temperature": 0.0, "max_tokens": 256}
)

evaluator = load_evaluator("qa", llm=evaluator_llm)

# Evaluate each model’s response to each prompt
print("\n🔍 Starting evaluation...\n")
for model_name, responses in all_responses.items():
    print(f"\nModel: {model_name}")
    for entry in responses:
        try:
            eval_result = evaluator.evaluate_strings(
                prediction=entry["response"],
                input=entry["prompt"],
                reference=None  # You can provide ground-truth if desired
            )
            print(f"- Prompt: {entry['prompt']}")
            print(f"  Response: {entry['response']}")
            print(f"  Eval Score: {eval_result.get('score', 'N/A')}\n")
        except Exception as e:
            print(f"Error evaluating {model_name} on prompt '{entry['prompt']}': {e}")

print("\n✅ Evaluation complete.")
with open("llm_outputs_eval.json", "w", encoding="utf-8") as f:
    json.dump(all_responses, f, indent=2, ensure_ascii=False)

print("✅ Responses saved to llm_outputs_eval.json")