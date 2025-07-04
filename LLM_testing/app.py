import requests
from langchain.llms import OpenAI
from langchain.evaluation.qa import QAEvalChain

# Replace these with your actual API endpoints and keys for each LLM
LLM_API_URL_1 = "https://api.llm1.com/generate"
LLM_API_URL_2 = "https://api.llm2.com/generate"
LLM_API_URL_3 = "https://api.llm3.com/generate"

HEADERS_1 = {"Authorization": "Bearer YOUR_LLM1_API_KEY"}
HEADERS_2 = {"Authorization": "Bearer YOUR_LLM2_API_KEY"}
HEADERS_3 = {"Authorization": "Bearer YOUR_LLM3_API_KEY"}

# Define the question you want to ask
question = "What is the capital of France?"
payload = {"prompt": question}

def get_llm_response(url, headers, payload):
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        # Assuming the API returns a JSON with an 'output' field containing the response
        return response.json().get("output", "").strip()
    except Exception as e:
        print(f"Error calling API at {url}: {e}")
        return ""

# Query each LLM
response1 = get_llm_response(LLM_API_URL_1, HEADERS_1, payload)
response2 = get_llm_response(LLM_API_URL_2, HEADERS_2, payload)
response3 = get_llm_response(LLM_API_URL_3, HEADERS_3, payload)

# For this example, we'll assume we know the ground truth answer
ground_truth = "Paris"

# Prepare evaluation examples for each LLM's output
examples = [
    {"query": question, "answer": ground_truth, "result": response1},
    {"query": question, "answer": ground_truth, "result": response2},
    {"query": question, "answer": ground_truth, "result": response3},
]

# Initialize an evaluator LLM (using OpenAI as an example; can be replaced with any supported LLM)
# This evaluator acts as our "meta-LLM" to score each response
evaluator_llm = OpenAI(temperature=0, api_key="YOUR_OPENAI_API_KEY")

# Create the QA evaluation chain
eval_chain = QAEvalChain.from_llm(evaluator_llm)

# Evaluate the outputs against the ground truth
graded_outputs = eval_chain.evaluate(examples, examples)

# Display the evaluation results
for i, eg in enumerate(examples):
    print(f"Example {i + 1}:")
    print("Question: " + eg["query"])
    print("Ground Truth: " + eg["answer"])
    print("LLM Output: " + eg["result"])
    print("Evaluation: " + graded_outputs[i]["text"])
    print("-" * 50)
