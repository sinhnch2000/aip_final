from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model_int = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
model_int.load_state_dict(torch.load("C:\ALL\FPT\AIP\\aip_final\checkpoint\ckpt_int.bin"))
embedding_size_int = model_int.get_input_embeddings().weight.shape[0]
if len(tokenizer) > embedding_size_int:
    model_int.resize_token_embeddings(len(tokenizer))

sample_int = {
    "instruction": "Provide information: ## History: {history} ## Current: {current} ## Ontology: {ontology}. The goal of this assignment is to determine the intent of the user in this conversation? It must use all the provided information.",
    "ontology": "hotels_1:[intent0=Reserve a selected hotel for given dates | intent1=Find a hotel at a given location]",
    "history": "",
    "current": ""
}
while(1):
    item_res = sample_int['instruction'].replace('{current}', "USER: " + input("input user:")) \
                                        .replace('{history}', input("input context:")) \
                                        .replace('{ontology}', sample_int['ontology'].strip())
    print(item_res)
    input_tokens = tokenizer(item_res, return_tensors="pt")
    output = model_int.generate(input_tokens["input_ids"], attention_mask=input_tokens["attention_mask"],
                                    max_new_tokens=100)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    print("response:", response)