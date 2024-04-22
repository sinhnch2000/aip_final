# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)
text = "You are SYSTEM, response with answer Query of USER based 1 part on context about under 10 words: context: SYSTEM: It is an entertainment attraction. Would you like their phone number and address? USER: Just the postcode please SYSTEM: The post code is cb58hy. Is there anything else I can do for you? Query: USER: Nope. I just want to get away from work."
input_tokens = tokenizer(text, return_tensors="pt")
output = model.generate(input_tokens["input_ids"], attention_mask=input_tokens["attention_mask"],
                                    max_new_tokens=100)
data_dst_1 = tokenizer.decode(output[0], skip_special_tokens=True)
print(data_dst_1)