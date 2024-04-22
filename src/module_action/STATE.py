import re

class STATE:
    def __init__(self, intent_schema, ontology, domain):
        self.list_action = ["inform", "request","inform_intent", "negate_intent", "affirm_intent", "affirm", "negate", "select", "thank_you", "goodbye", "greet", "general_asking", "request_alts"]
        self.classify_dst = ""
        self.domain = domain

        self.after_output_dst = {}
        self.user_intent = "NONE"
        self.ontology = ontology
        # ontology = {description_0:[slot00, slot01],
        #             description_1:[slot10, slot11],
        #             description_2:[slot20]}
        self.map_ontology = dict()
        for i in range(len(ontology)):
            self.map_ontology.setdefault("slot"+str(i), list(self.ontology.values())[i])
        # map_ontology = {slot_0:[slot00, slot01],
        #                 slot_1:[slot10, slot11],
        #                 slot_2:[slot20]}
        self.intent_schema = intent_schema
        self.offer_slots = []
        self.db_slots = []
        self.offer_slots = []
        self.output_paper = ""
        # intent_schema = {intent_0:{description_0:[slot0]},
        #                  intent_1:{description_1:[slot0, slot1, slot2]},
        #                  another:{"":[slot3, slot4]}}
        for i in range(len(self.intent_schema)):
            intent = list(self.intent_schema.keys())[i]
            description_listSlots = list(self.intent_schema.values())[i]
            description = list(description_listSlots.keys())[0]
            listSlots = list(description_listSlots.values())[0]
            for i in range(len(listSlots)):
                slot_in_intent = listSlots[i]
                for slot_digit, list_slot_in_map_ontology in self.map_ontology.items():
                    if slot_in_intent in list_slot_in_map_ontology:
                        self.intent_schema[intent][description][i] = slot_digit
        self.list_action_for_intent = {
            "search_one":["searchoneway"],
            "search_round":["searchroundtrip"],
            "book_one":["reserveoneway"],
            "book_round":["reserveroundtrip"],
            "search":["search", "find", "getcar"],
            "add":["add"],
            "time": ["time"],
            "get":["get", "check"],
            "sent":["transfer", "share", "pay"],
            "play":["play"],
            "book":["book", "reserve", "buy", "rent"]
        }
        self.reset_slots(self.map_ontology)
        self.map_intent_schema = {}
        for intent, description_listSlots in self.intent_schema.items():
            for description, listSlots in description_listSlots.items():
                for new_intent, list_old_intent in self.list_action_for_intent.items():
                    for old_intent in list_old_intent:
                        if old_intent in intent.lower():
                            intent = new_intent
                            break
                    if intent == new_intent:
                        break
                self.map_intent_schema.setdefault(intent, listSlots)

    def reset_slots(self, map_ontology):
        # map_ontology = {slot_0:[slot00, slot01],
        #                 slot_1:[slot10, slot11],
        #                 slot_2:[slot20]}
        self.slots = {slotdigit: None for slotdigit, listslots in map_ontology.items()}
        # slots = {slot_0:None,
        #          slot_1:None,
        #          slot_2:None}

    def convert_str_to_int(self, string):
        english_to_number_dict = {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
            "ten": 10,
        }
        try:
            float(string)
            return float(string)
        except ValueError:
            pass

        string = string.strip()
        for str, int in english_to_number_dict.items():
            if string.lower() == str:
                return float(int)
        return string

    def convert_output_dst(self, before_output_dst):
        self.after_output_dst.clear()
        # edit action
        list_action_no_slot = ["negate_intent", "affirm_intent", "affirm", "thank_you", "goodbye", "greet", "negate", "select", "request_alts"]
        for action in list_action_no_slot:
            if action in before_output_dst:
                if (action == "negate" and "negate_intent" in before_output_dst) or (action == "affirm" and "affirm_intent" in before_output_dst):
                    continue
                before_output_dst = before_output_dst.replace(action, action+"(none|none)")

        before_output_dst = re.sub(r"request\((slot\d+)\)", lambda match: f"request({match.group(1)}|none)", before_output_dst)
        before_output_dst = re.sub(r"inform_intent\((\w+)\)", lambda match: f"inform_intent(intent|{match.group(1)})",before_output_dst)
        before_output_dst = re.sub(r"inform\((slot\d+)=(\w+)", lambda match: f"inform({match.group(1)}|{match.group(2)}", before_output_dst)

        # complete general asking
        before_output_dst = before_output_dst.replace("general_asking", "asking>none|none").replace("chitchat", "asking>none|none")

        if "asking>" in before_output_dst:
            if "asking" not in self.after_output_dst.keys():
                self.after_output_dst.setdefault("asking", {"none":"none"})
        elif before_output_dst == "":
            self.after_output_dst.append("")
        else:
            # classify base on domain
            list_domain_infor = before_output_dst.split("||")
            for domain_infor in list_domain_infor:

                # divide domain / action_slot_value
                domain_infor = domain_infor.strip()[:-1].split(":[")
                all_action_slot_value = domain_infor[1][:-1]
                # divide action_slot_value
                list_action_slot_value = all_action_slot_value.split(") and ")

                for action_slot_value in list_action_slot_value:

                    # analyze action_slot_value
                    for action in self.list_action:
                        if action+"(" in action_slot_value:
                            action_slot_value = action_slot_value.replace(action + "(", action + ">")
                            action_slot_value = action_slot_value.split(">")
                            action = action_slot_value[0].lower()
                            slot_value = action_slot_value[1]
                            slot_value = slot_value.split("|")
                            slot = slot_value[0].lower()
                            value = slot_value[1]
                            if action not in self.after_output_dst.keys():
                                self.after_output_dst.setdefault(action, {})
                            if slot not in self.after_output_dst[action].keys():
                                self.after_output_dst[action].setdefault(slot, None)
                            self.after_output_dst[action][slot] = value
                            # after_output_dst = {action0:{slot0:value0, slot1:value1},
                            #                     action1:{slot2:value2},
        if "inform_intent" in self.after_output_dst.keys():
            for new_intent, list_old_intent in self.list_action_for_intent.items():
                for old_intent in list_old_intent:
                    if old_intent in self.after_output_dst["inform_intent"]["intent"].lower():
                        self.after_output_dst["inform_intent"]["intent"] = new_intent
                        break
            if self.user_intent == self.after_output_dst["inform_intent"]["intent"]:
                del self.after_output_dst["inform_intent"]
            elif (self.after_output_dst["inform_intent"]["intent"] == "search" and self.user_intent == "book"):
                del self.after_output_dst["inform_intent"]

        if "inform_intent" in self.after_output_dst.keys():
            self.user_intent = self.after_output_dst["inform_intent"]["intent"]
            for new_intent, list_old_intent in self.list_action_for_intent.items():
                for old_intent in list_old_intent:
                    if old_intent in self.user_intent.lower():
                        self.user_intent = new_intent
                        break

    def convert_to_output_paper(self):
        type = "TOD"
        current_action = ""
        current_state = ""
        list_current_action = []
        list_current_state = []
        for action, list_slot_value in self.after_output_dst.items():
            if action in ["thank_you", "goodbye", "greet"]:
                type = "ODD"
            for slot, value in list_slot_value.items():
                if action == "request" and value.lower() == "none":
                    list_current_action.append(action+">"+self.domain.lower()+"-"+slot+"-"+"?")
                else:
                    list_current_action.append(action+">"+self.domain.lower()+"-"+slot+"-"+value.lower())
        for slot, value in self.slots.items():
            if value != None:
                list_current_state.append(self.domain.lower()+"-"+slot+"-"+str(value).lower())
        current_action+="\n".join(list_current_action)
        current_state +="\n".join(list_current_state)
        self.output_paper = "(TYPE) " + type + "\n\n(CURRENT ACTION)\n" + current_action + "\n\n(CURRENT STATE)\n"+ current_state

    def update_slot(self):
        if "inform" in self.after_output_dst.keys():
            for slot, value in self.after_output_dst["inform"].items():
                if value != self.slots[slot] and value != None:
                    self.slots.update(self.after_output_dst["inform"])
