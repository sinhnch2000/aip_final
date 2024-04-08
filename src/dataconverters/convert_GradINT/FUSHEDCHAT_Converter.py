import sys
import json
import random
import glob
import os
from typing import List, Dict, Union, Optional
from src.dataconverters.converter import DialConverter

sys.path.append('/content/drive/MyDrive/Colab Notebooks/baseline_v1/gradients.baselinev1.dialogstate')
list_woz_domain = ['taxi', 'police', 'hospital', 'hotel', 'attraction', 'train', 'restaurant']

class FushedChatConverter(DialConverter):
    def __init__(self,
                 file_path: str,
                 save_path: str,
                 tag_user: str = 'USER',
                 tag_system: str = 'SYSTEM',
                 ) -> None:
        """
        Args:
            save_path: path to save the processed dataset
        """
        super().__init__(file_path, save_path, tag_user, tag_system)

    def __call__(self, instruction_path, ontolopy_path):
        print(f"Start  processing {self.__class__.__name__}")
        self.process(instruction_path=instruction_path, ontolopy_path=ontolopy_path)
        print(f"Finish processing {self.__class__.__name__} at {self.save_path}")

    def process(self, instruction_path, ontolopy_path):
        # Separate complete dialogues to sub dialogues
        list_data_path = glob.glob(os.path.join(self.file_path,'*.json'))
        list_instruction = self.load_instruction(instruction_path)
        list_ontology = self.load_ontology(ontolopy_path)

        for data_path in list_data_path:
            filename = os.path.basename(data_path)
            dataset = self.load_datapath(data_path)

            list_all_sample = []
            # Analyze all dialogues
            for id, dialogue in dataset.items():

                # get summarize dialogue
                list_gold_domain = self.get_list_gold_domain(dialogue, list_ontology)
                # process dialogue into sub-dialogues
                list_sub_dialogue = []
                for i in range(len(dialogue['log'])):
                    if i % 2 == 0:
                        list_sub_dialogue.append(dialogue['log'][0:i+1])
                # process raw list_sub_dialogue to interim list_sub_sample
                list_sub_sample = self.get_list_sub_sample(id, list_sub_dialogue, list_gold_domain, list_ontology, list_instruction)
                list_all_sample.extend(list_sub_sample)
            self.save_datapath(list_all_sample, filename)

    def get_list_sub_sample(self, id, list_sub_dialogue, list_gold_domain, list_ontology, list_instruction):
        list_sub_sample = []
        dict_state_one_dialogue = dict()
        for id_turn, sub_dialogue in enumerate(list_sub_dialogue):
            item = dict()
            list_intent_label = set()

            # get context, current_user, instruction and ontology
            list_turn = []
            for turn in sub_dialogue:
                speaker = self.tag_user if turn['speaker'] == 'USER' else self.tag_system
                turn["text"] = turn["text"].strip()
                if turn["text"][-1] not in [".", "?", "!", ";"]:
                    turn["text"] = turn["text"] + "."
                list_turn.append(speaker + ": " + turn['text'])

            item['instruction'] = self.get_instruction(list_instruction).strip()
            item['ontology'] = ' & '.join(gold_domain for gold_domain in list_gold_domain).strip()
            item['history'] = ' '.join([list_turn[i].strip() for i in range(len(list_turn)-1)]).strip()
            item['current'] = list_turn[-1].strip()
            item['id_dialogue'] = id
            item['id_turn'] = id_turn*2 + 1

            if "intent" in sub_dialogue[-1].keys():
                list_domain_intent = sub_dialogue[-1]["intent"]
                for domain_intent_real in list_domain_intent:
                    intent_real = domain_intent_real.split("-")[1]
                    domain_real = domain_intent_real.split("-")[0]
                    onto_mapping = self.map_ontology(domain_real, list_ontology)
                    for intent, intentDigit_description in onto_mapping.items():
                        if intent_real == intent:
                            intent_real = list(intentDigit_description.keys())[0]
                    if "intent" not in intent_real:
                        print(domain_intent_real)
                    list_intent_label.add(domain_real+"-"+intent_real)
            else:
                list_intent_label.add("NONE")

            item['label'] = (" | ").join(p for p in list(list_intent_label))
            list_sub_sample.append(item)

        return list_sub_sample

    # LOAD and SAVE data
    def load_datapath(self, data_path) -> List[Dict]:
        with open(data_path, 'r+') as f:
            dataset = json.load(f)
        return dataset

    def save_datapath(self, data_processed: List[Dict], filename: str):
        with open(os.path.join(self.save_path, filename), 'w') as f:
            json.dump(data_processed, f, indent=4)

    # LOAD and GET instruction
    def load_instruction(self, instruct_path) -> List[str]:
        with open(instruct_path, encoding="utf8") as f:
            instructions = f.readlines()
        return instructions

    def get_instruction(self, list_instructions):
        random_instruction = list_instructions[random.randint(0, len(list_instructions) - 1)]
        return random_instruction

    # LOAD and MAP and GET ontology
    def load_ontology(self, ontolopy_path: Optional[str] = None) -> Union[Dict, List[Dict]]:
        with open(ontolopy_path, encoding="utf8") as f:
            ontologies = json.load(f)
        return ontologies

    def map_ontology(self, domain, ontologies, count=0):
        map_ontology_domain = {}
        for intent, description_requiredslot in ontologies[domain].items():
            description = list(description_requiredslot.keys())[0]
            map_ontology_domain.setdefault(intent, {"intent"+str(count):description})
            count = count + 1
        return map_ontology_domain
        # {"SearchHouse":{"intent0": "Find a house at a given location"},
        #  "BookHouse":{"intent1": "Book the selected house for given dates and number of adults"}}

    def get_ontology(self, domain_name, ontologies):
        onto_mapping = self.map_ontology(domain_name, ontologies)
        tmps = []
        for intent, intentDigit_description in onto_mapping.items():
            tmps.append(list(intentDigit_description.keys())[0] + "=" + list(intentDigit_description.values())[0])

        value_onto = domain_name + ":[" + ' | '.join(tmp for tmp in tmps) + "]"
        return value_onto, onto_mapping
        # value_onto = DOMAIN:(intent0=des0, intent1=des1, intent2=des2)

    def get_list_gold_domain(self, dialogue, ontology):
        gold_domain = []
        tmp_domain = set()
        goal = dialogue["goal"]
        for domain, all_info in goal.items():
            if domain not in ["message", "topic"] and all_info != {}:
                if "info" in all_info.keys():
                    tmp_domain.add(domain.lower())
        for domain in tmp_domain:
            if domain in list_woz_domain:
                value_onto,_ = self.get_ontology(domain, ontology)
                gold_domain.append(value_onto)
        return gold_domain


if __name__ == '__main__':
    # TEST
    fusedchat_converter = FushedChatConverter(
        file_path=r'C:\ALL\FPT\AIP\aip_final\data\raw\FUSEDCHAT\after_intent',
        save_path=r'C:\ALL\FPT\AIP\aip_final\data\interim\GradINT\FUSEDCHAT').__call__(
        instruction_path=r"C:\ALL\FPT\AIP\aip_final\data\instruction\instruct_GradINT.txt",
        ontolopy_path=r"C:\ALL\FPT\AIP\aip_final\data\schema\intent_schema.json")







