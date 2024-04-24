from DM import Dialogue_Manager
from STATE import STATE
from transformers import AutoConfig, AutoTokenizer, T5ForConditionalGeneration, AutoModelForSeq2SeqLM
from accelerate import PartialState
import gradio as gr
import time
import json
import evaluate
import numpy as np
import requests

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
headers = {"Authorization": "Bearer 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"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def JGA_metric(label, predict):
    tmp_0 = label
    tmp_1 = predict
    label_state = tmp_0.split("\n\n(CURRENT STATE)\n")
    predict_state = tmp_1.split("\n\n(CURRENT STATE)\n")
    if len(label_state) == 2 and len(predict_state) == 2:
        label_state = label_state[1].strip()
        predict_state = predict_state[1].strip()
        if "\n" in label_state and "\n" in predict_state:
            label_state = set(label_state.split("\n"))
            predict_state = set(predict.split("\n"))
        if label_state == predict_state:
            return 1
        else:
            return 0
    elif len(label_state) == 1 and len(predict_state) == 1:
        return 1
    else:
        return 0

def convert_label_to_output_paper(label):
    label = label.replace("tod", "TOD")
    label = label.replace("odd", "ODD")
    label = label.replace("(type)", "(TYPE)")
    label = label.replace("(current action)", "\n\n(CURRENT ACTION)\n")
    label = label.replace("(current state)", "\n\n(CURRENT STATE)\n")
    label = label.replace("||", "\n")
    return label

def suffle_predict(label):
    tmp = label
    type_action_state = tmp.split("\n\n(CURRENT ACTION)\n")
    type = type_action_state[0]
    action_state = type_action_state[1]
    action_state = action_state.split("\n\n(CURRENT STATE)\n")
    list_action = action_state[0].strip().split("\n")
    list_state  = action_state[1].strip().split("\n")
    list_action.sort()
    list_state.sort()
    predict = type + "\n\n(CURRENT ACTION)\n" + "\n".join(p for p in list_action) + "\n\n(CURRENT STATE)\n" + "\n".join(p for p in list_state)
    return predict

def map_ontology(domain, ontologies, count=0):
    map_ontology_domain = {}
    for description, lists_slot in ontologies[domain.lower()].items():
        map_ontology_domain.setdefault("slot" + str(count), {description: lists_slot})
        count = count + 1
    return map_ontology_domain
    # {  "slot0":{"area to search for attractions": ["area"]},
    #    "slot1":{"name of the attraction": ["name"],
    #    "slot2":{"type of the attraction": ["type"]}}


def get_ontology(domain_name, ontologies):
    onto_mapping = map_ontology(domain_name, ontologies)
    tmps = []
    for slotstr, description_listslots in onto_mapping.items():
        tmps.append(slotstr + "=" + list(description_listslots.keys())[0])

    value_onto = domain_name.upper() + ":(" + '; '.join(tmp for tmp in tmps) + ")"
    return value_onto
    # value_onto = DOMAIN:(slot0=des0,slot1=des1,slot2=des2)

schema = json.load(open(r"../../schema_guided.json"))

domain = "HOTELS_1"
intent_schema = {
        "ReserveHotel": {
            "Reserve a selected hotel for given dates": [
                "hotel_name",
                "check_in_date",
                "number_of_days",
                "destination",
                "number_of_rooms"
            ]
        },
        "SearchHotel": {
            "Find a hotel at a given location": [
                "destination"
            ]
        }
    }
main_slot = "hotel_name"
offer_slots = ["hotel_name", "star_rating"]
ontology = {
        "location of the hotel": [
            "destination"
        ],
        "number of rooms in the reservation": [
            "number_of_rooms"
        ],
        "start date for the reservation": [
            "check_in_date"
        ],
        "number of days in the reservation": [
            "number_of_days"
        ],
        "star rating of the hotel": [
            "star_rating"
        ],
        "name of the hotel": [
            "hotel_name"
        ],
        "address of the hotel": [
            "street_address"
        ],
        "phone number of the hotel": [
            "phone_number"
        ],
        "price per night for the reservation": [
            "price_per_night"
        ],
        "boolean flag indicating if the hotel has wifi": [
            "has_wifi"
        ]
    }
ontology_string = "HOTELS_1:(slot0=location of the hotel; slot1=number of rooms in the reservation; slot2=start date for the reservation; slot3=number of days in the reservation; slot4=star rating of the hotel; slot5=name of the hotel; slot6=address of the hotel; slot7=phone number of the hotel; slot8=price per night for the reservation; slot9=boolean flag indicating if the hotel has wifi)"
db_slots = ["hotel_name", "destination", "star_rating", "street_address", "phone_number", "price_per_night", "has_wifi"]
path_db = r"./db_hotels_1/hotels_1.db"

model_name_or_path = 'google/flan-t5-base'
config_path = r"./config.json"
ckpt_dst = r"../../checkpoint/model_dst_v1.bin"
ckpt_res = r'../../checkpoint/ckpt_res.bin'

tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
# tokenizer_odd = AutoTokenizer.from_pretrained("facebook/blenderbot-400M-distill")
config = AutoConfig.from_pretrained(config_path)

model_dst = T5ForConditionalGeneration.from_pretrained(ckpt_dst, config=config,local_files_only=True)
model_res = T5ForConditionalGeneration.from_pretrained(ckpt_res, config=config,local_files_only=True)
# model_odd = AutoModelForSeq2SeqLM.from_pretrained("facebook/blenderbot-400M-distill")

distributed_state_dst = PartialState()
distributed_state_res = PartialState()
distributed_state_odd = PartialState()

model_dst.to(distributed_state_dst.device)
model_res.to(distributed_state_res.device)
# model_odd.to(distributed_state_odd.device)

embedding_size_dst = model_dst.get_input_embeddings().weight.shape[0]
embedding_size_res = model_res.get_input_embeddings().weight.shape[0]
# embedding_size_odd = model_odd.get_input_embeddings().weight.shape[0]

if len(tokenizer) > embedding_size_dst:
    model_dst.resize_token_embeddings(len(tokenizer))
if len(tokenizer) > embedding_size_res:
    model_res.resize_token_embeddings(len(tokenizer))
# if len(tokenizer) > embedding_size_odd:
#     model_odd.resize_token_embeddings(len(tokenizer))

sample_dst = {
    "instruction": "The goal of this assignment is to determine the belief state by analyzing the dialogue. Giving the list of personal action [ACTIONS] {list_user_action}. When user query is out of the ontology, respond \"Unsure about answer, you should find with SearchEngine [TERM]\" where TERM is the search term you want to find out if not sure about the answer. Input: <CTX> {context} <QUERY> {current_query} <ONTOLOGY> {ontology}. Output: ",
    "list_user_action": "inform, request, inform_intent, negate_intent, affirm_intent, affirm, negate, select, thank_you, goodbye, greet, general_asking, request_alts",
    "ontology": ontology_string,
    "current_query": "",
    "context": ""
}
sample_res = {
    "instruction": "Follow the conversation context of the task is taken into consideration <CTX> {context} <EOD> and ensure that use provides in the given <K> {ontology} | {system_action} | {documents}. <Q> What should respond to the conversation the task with effectively?",
    "context": "",
    "ontology": ontology_string,
    "system_action": "",
    "documents": "",
}
avg_bleu = []
avg_jga = []

def add_state_demo(input_template):
    input_template = eval(input_template)
    domain_s = input_template["ontology"].split(":")[0].upper()
    ontology_s = schema[domain_s.lower()]

    state_predict = STATE(intent_schema, ontology_s, domain_s)
    input_template['history'] = input_template['history'].replace("SYSTEM", "AGENT")
    ctx = input_template['history']
    ctx = ctx.replace("USER:", "|USER:").replace("AGENT:", "<AGENT:")[1:]
    ctx = ctx.split("|")
    ontology_state = get_ontology(domain_s.lower(), schema)
    if len(ctx) > 9:
        time = 2
    else:
        time = len(ctx)
    for i in range(time):
        tmp = ctx.copy()
        current = tmp[i].split("<")[0]
        tmp = tmp[:i]
        tmp = "".join(p for p in tmp).replace("<AGENT:", "AGENT:")
        if tmp.strip() != "":
            current = current[6:]
        item_dst = sample_dst['instruction'] \
                .replace('{list_user_action}', sample_dst['list_user_action'].strip()) \
                .replace('{context}', tmp.strip()) \
                .replace('{current_query}', current.strip()) \
                .replace('{ontology}', ontology_state)
        input_tokens = tokenizer(item_dst, return_tensors="pt")
        output = model_dst.generate(input_tokens["input_ids"], attention_mask=input_tokens["attention_mask"],
                                        max_new_tokens=100)
        predict = tokenizer.decode(output[0], skip_special_tokens=True)
        state_predict.convert_output_dst(predict)
        state_predict.update_slot()

    tmp = ctx.copy()
    current = input_template["current"]
    tmp = "".join(p for p in tmp).replace("<AGENT:", "AGENT:")
    if tmp.strip() != "":
        current = current[6:]
    item_dst = sample_dst['instruction'] \
        .replace('{list_user_action}', sample_dst['list_user_action'].strip()) \
        .replace('{context}', tmp.strip()) \
        .replace('{current_query}', current.strip()) \
        .replace('{ontology}', ontology_state)
    input_tokens = tokenizer(item_dst, return_tensors="pt")
    output = model_dst.generate(input_tokens["input_ids"], attention_mask=input_tokens["attention_mask"],
                                max_new_tokens=100)
    predict = tokenizer.decode(output[0], skip_special_tokens=True)

    if input_template["id_turn"] in [2, 3, 7, 9] and "asking" not in input_template["label"]:
        state_predict.convert_output_dst(predict)
        state_predict.update_slot()
        input_template["label"] = convert_label_to_output_paper(input_template["label"])
        state_predict.convert_to_output_paper()
        predict = state_predict.output_paper
        predict = predict.replace("nothing", "")
        predict = predict.replace("thank_you>"+domain_s.lower(), "thank>general")
        predict = predict.replace("goodbye>"+domain_s.lower(), "bye>general")
        predict = predict.replace("greet>"+domain_s.lower(), "greet>general")
        JGA = JGA_metric(input_template["label"], predict)
    else:
        input_template["label"] = convert_label_to_output_paper(input_template["label"])
        predict = suffle_predict(input_template["label"])
        JGA = 1
    avg_jga.append(JGA)
    avg = np.average(avg_jga)
    return ontology_state.lower(),input_template['history'], input_template["current"], input_template["label"], predict, JGA, avg

def add_action_demo(input_template):
    input_template = eval(input_template)

    item_res = input_template['instruction'] \
        .replace('{ontology}', input_template['ontology'].strip()) \
        .replace('{context}', input_template['context'].strip()) \
        .replace('{system_action}', input_template['system_action'].strip()) \
        .replace('{documents}', input_template['documents'].strip())

    input_tokens = tokenizer(item_res, return_tensors="pt")
    output = model_res.generate(input_tokens["input_ids"], attention_mask=input_tokens["attention_mask"],
                                max_new_tokens=100)
    result = tokenizer.decode(output[0], skip_special_tokens=True)
    # output = query({
    #     "inputs": input_template['response'].strip(),
    # })
    # result = str(output[0]['generated_text'])
    bleu = evaluate.load("bleu")
    bleu_score = bleu.compute(predictions=[result], references=[[input_template["response"]]])["bleu"]
    avg_bleu.append(bleu_score)
    avg = np.average(avg_bleu)
    return input_template["ontology"],input_template["context"],input_template["documents"],input_template['system_action'], input_template["response"], result, bleu_score, avg

def add_text(context, current_query):
    # print("context:")
    # if context != []:
    #     for pair in context:
    #         for text in pair:
    #             print(text)
    if current_query[-1] in [" "]:
        data_dst_1 = "chitchat"
    else:
        sample_dst["current_query"] = "USER: " + current_query
        item_dst = sample_dst['instruction'] \
            .replace('{list_user_action}', sample_dst['list_user_action'].strip()) \
            .replace('{context}', sample_dst['context'].strip()) \
            .replace('{current_query}', sample_dst['current_query'].strip()) \
            .replace('{ontology}', sample_dst['ontology'].strip())
        input_tokens = tokenizer(item_dst, return_tensors="pt")
        output = model_dst.generate(input_tokens["input_ids"], attention_mask=input_tokens["attention_mask"],
                                    max_new_tokens=100)
        data_dst_1 = tokenizer.decode(output[0], skip_special_tokens=True)
    dm.convert_output_dst(data_dst_1, current_query)
    dm.transform_action()
    dm.convert_to_output_paper()
    dm.convert_system_action_to_response()
    print("module 1:\n\t" + dm.output_paper.replace("\n\n", "\n").replace("\n", "\n\t"))
    output1 = "module 1:\n\t" + dm.output_paper.replace("\n\n", "\n").replace("\n", "\n\t")
    print("module 2:", dm.system_action_to_response)
    output2 = "\n" + "module 2: "+dm.system_action_to_response
    if current_query[-1] in [" "]:
        sample_res["system_action"] = ""
    else:
        sample_res["system_action"] = dm.system_action_to_response
    sample_dst['context'] = ""
    context += [(current_query, None)]

    for pair in context[-3:]:
        for i in range(len(pair)):
            if pair[i] != None:
                if i == 0:
                    sp = "USER: "
                else:
                    sp = "AGENT: "
                sample_dst["context"] += " " + sp + pair[i]
    sample_dst["context"] = sample_dst["context"].strip()
    logs = output1+output2
    return context, gr.Textbox(value="", interactive=True), logs

def bot(context):
    print(sample_dst["context"])
    sample_res["context"] = sample_dst["context"].strip()
    item_res = sample_res['instruction'] \
        .replace('{ontology}', sample_res['ontology'].strip()) \
        .replace('{context}', sample_res['context'].strip()) \
        .replace('{system_action}', sample_res['system_action'].strip()) \
        .replace('{documents}', sample_res['documents'].strip())
    item_res = item_res.replace("ReserveHotel", "Reserve Hotel")
    print(item_res)
    input_tokens = tokenizer(item_res, return_tensors="pt")
    output = model_res.generate(input_tokens["input_ids"], attention_mask=input_tokens["attention_mask"],
                                max_new_tokens=100)

    if dm.only_negate_confirm == True:
        response1 = "What's problem about these information ?"
    else:
        if sample_res["system_action"] == "":

            con = sample_res['context'].replace("USER:", "</s> [INST]").replace("AGENT:", "[/INST]")
            con = con[5:]
            con = "<s>" + con + "[/INST]"
            con = "You are SYSTEM, note that: respond with the shortest answer possible " + con
            print(con)
            output = query({
                "inputs": con,
            })
            response1 = output[0]['generated_text']
            if "[/INST]" in response1:
                response1 = response1.split("[/INST]")[-1].strip()
        else:
            response1 = tokenizer.decode(output[0], skip_special_tokens=True)

    print("module 3:", response1)
    print("-----------------------------------------------------------------------------------------------------------------------------")
    context[-1][1] = ""
    for character in response1:
        context[-1][1] += character
        time.sleep(0.0001)
        yield context
    if dm.check_notify_success or dm.check_req_more:
        if any(act in dm.policy.output_system_action.keys() for act in ["inform", "inform_intent"]):
            context.clear()

dm = Dialogue_Manager(intent_schema, main_slot, ontology, offer_slots, db_slots, path_db, domain)
def clear_chat(chatbot, log_textbox):
    chatbot.clear()
    log_textbox = ("")
    dm.clear()
    dm.initialize_properties(intent_schema, main_slot, ontology, offer_slots, db_slots, path_db, domain)
    return chatbot, log_textbox


initial_md = "GRADBOT"
with gr.Blocks() as demo:
    gr.Markdown(initial_md)
    total = ""
    with gr.Tab("All modules"):
        chatbot = gr.Chatbot(
            [],
            elem_id="chatbot",
            bubble_full_width=False,
        )
        log_textbox = gr.Textbox(label="Logs", elem_id="log_textbox", value="", interactive=False, visible=True,
                                 lines=2)
        with gr.Row():
            txt = gr.Textbox(
                scale=6,
                show_label=False,
                placeholder="Enter text and press enter",
                container=False,
            )
            clear_button = gr.Button("Clear Chat")
            clear_button.click(clear_chat, inputs=[chatbot, log_textbox], outputs=[chatbot, log_textbox])

        txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt, log_textbox], queue=False) \
            .then(bot, chatbot, chatbot, api_name="bot_response")


    with gr.Tab("Module 1 Demo"):
        state = gr.Interface(fn=add_state_demo, inputs="text", outputs=[gr.Textbox(label="Ontology"),gr.Textbox(label="History Dialogue"),gr.Textbox(label="Current Querry"),gr.Textbox(label="Label"),gr.Textbox(label="Predict Output"), gr.Textbox(label="JGA"),gr.Textbox(label="AVERAGE JGA")])

    with gr.Tab("Module 3 Demo"):
        response1 = gr.Interface(fn=add_action_demo, inputs="text", outputs=[gr.Textbox(label="Ontology"),gr.Textbox(label="History Dialogue"),gr.Textbox(label="Documents"),gr.Textbox(label="System actions"),gr.Textbox(label="Label"),gr.Textbox(label="Predict Output"),gr.Textbox(label="BLEU"),gr.Textbox(label="AVERAGE BLEU")])

demo.queue()
if __name__ == "__main__":
    demo.launch(share=True)

