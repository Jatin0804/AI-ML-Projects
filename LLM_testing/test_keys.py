import requests

# API_URI = "https://api-inference.huggingface.co/models/"
HEADERS = {"Authorization": "Bearer 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"}


MODELS = [
    "gpt2",  # Small, baseline model
    "tiiuae/falcon-7b-instruct",  # Instruction-tuned model
    "mistralai/Mistral-7B-Instruct-v0.1",  # Open-weight model
    "HuggingFaceH4/zephyr-7b-beta" # Chat-tuned model from HF
]
    


# payload = {
#     "inputs": "What is the future of artificial intelligence?",
#     "parameters": {"max_new_tokens": 50}
# }

# def get_llm_response(url, headers, payload):
#     try:
#         response = requests.post(url, json=payload, headers=headers)
#         response.raise_for_status()
#         # Assuming the API returns a JSON with an 'output' field containing the response
#         return response.json()
#     except Exception as e:
#         print(f"Error calling API at {url}: {e}")
#         return ""

# # Query each LLM
# response = get_llm_response(API_URI, HEADERS, payload)

def query_hf_model(model_id: str, prompt: str, max_new_tokens: int = 50):
    api_url = f"https://api-inference.huggingface.co/models/{model_id}"
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_new_tokens,
            "return_full_text": False
        }
    }
    try:
        response = requests.post(api_url, headers=HEADERS, json=payload, timeout=60)
        response.raise_for_status()
        output = response.json()
        return output[0]["generated_text"] if isinstance(output, list) else output
    except Exception as e:
        return f"Error from model {model_id}: {e}"

def get_outputs_from_models(prompt: str):
    results = {}
    for model in MODELS:
        print(f"Fetching response from: {model}")
        response = query_hf_model(model, prompt)
        results[model] = response
    return results

user_prompt = "Explain Gravity in simple terms."
responses = get_outputs_from_models(user_prompt)

for model_name, output in responses.items():
    print(f"\n--- {model_name} ---")
    print(output)