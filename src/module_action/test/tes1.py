import requests

API_URL = "https://api-inference.huggingface.co/models/humarin/chatgpt_paraphraser_on_T5_base"
headers = {"Authorization": "Bearer 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"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


output = query({
    "inputs": "how are you today",
})

print(output[0]['generated_text'])