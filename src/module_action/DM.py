import re
from POLICY import Policy
from utils import *
import random

class Dialogue_Manager:
    def __init__(self, intent_schema, main_slot, ontology, offer_slots, db_slots, path_db, domain):
        self.list_action = ["inform", "request","inform_intent", "negate_intent", "affirm_intent", "affirm", "negate", "select", "thank_you", "goodbye", "greet", "general_asking", "request_alts"]
        self.classify_dst = ""
        self.path_db = path_db
        self.domain = domain
        self.after_output_dst = {}
        self.user_intent = "NONE"
        self.offer_intent = ""
        self.dict_negate_request = {"request": {}}
        self.ontology = ontology
        self.change_search_slots = False
        self.change_main_slot = False
        self.check_confirm = False
        self.check_notify_success = False
        self.check_req_more = False
        self.only_negate_confirm = False
        self.requesting = False
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
        self.exist_main_slot = True
        self.output_paper = ""
        self.system_action_to_response = ""
        self.main_slot = ""
        for slotdigit, listSlots in self.map_ontology.items():
            for slot in db_slots:
                if slot in listSlots:
                    self.db_slots.append(slotdigit)
            if main_slot in listSlots:
                self.main_slot = slotdigit
            for slot in offer_slots:
                if slot in listSlots:
                    self.offer_slots.append(slotdigit)
        else:
            self.db_slots.append(slot)
        self.policy = Policy(self.map_ontology, self.main_slot, self.db_slots, self.path_db, self.domain)
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

    def convert_output_dst(self, before_output_dst, current):
        # edit action
        self.policy.output_system_action.clear()
        self.after_output_dst.clear()
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
                self.policy.output_system_action.setdefault("asking", {"none":"none"})
        elif before_output_dst == "":
            self.after_output_dst.append("")
        else:
            # classify base on domain
            list_domain_infor = before_output_dst.split("||")
            for domain_infor in list_domain_infor:

                # divide domain / action_slot_value
                domain_infor = domain_infor.strip()[:-1].split(":[")
                domain = domain_infor[0].lower()
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
        if self.only_negate_confirm == True and "inform" in self.after_output_dst.keys():
            self.only_negate_confirm = False
            if "negate" in self.after_output_dst.keys():
                del self.after_output_dst["negate"]

        if self.requesting:
            self.requesting = False
            if any(action in self.after_output_dst.keys() for action in ["inform", "request"]):
                tmp = list(self.after_output_dst.keys()).copy()
                for act in tmp:
                    if act in ["negate", "inform_intent"]:
                        del self.after_output_dst[act]
                    if act in ["affirm", "select", "affirm_intent"] and self.policy.dst.slots[self.main_slot] != None:
                        del self.after_output_dst[act]
            if any(act in self.after_output_dst.keys() for act in ["negate", "negate_intent"]) and self.policy.dst.slots[self.main_slot] == None:
                if self.user_intent == "":
                    self.set_offer_intent("search")
                else:
                    self.set_offer_intent("book")
                self.offer_new_intent()

        if self.offer_intent != "" and "affirm" in self.after_output_dst.keys() and self.check_confirm:
            del self.after_output_dst["request"]

        if "thank_you" in self.after_output_dst.keys() and "thank" not in current.lower():
            del self.after_output_dst["thank_you"]

    def convert_system_action_to_response(self):
        list_action = []
        if "inform" in self.policy.output_system_action.keys():
            for slot, value in self.policy.output_system_action["inform"].items():
                tmp = "inform" + ":(" + slot + "=" + str(value) + ")"
                list_action.append(tmp)
            del self.policy.output_system_action["inform"]

        for action, slot_value in self.policy.output_system_action.items():
            for slot, value in slot_value.items():
                tmp = ""
                if value == "none":
                    if slot == "none":
                        tmp = action
                    else:
                        tmp = action + ":(" + slot + ")"
                else:
                    tmp = action + ":(" + slot + "=" + str(value) + ")"
                list_action.append(tmp)
        self.system_action_to_response+=" and ".join(list_action)

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
                if slot in self.map_ontology.keys():
                    slot = self.map_ontology[slot][0]
                list_current_action.append(action+">"+self.domain.lower()+"-"+slot+"-"+value)
        for slot, value in self.policy.dst.slots.items():
            if slot in self.map_ontology.keys():
                slot = self.map_ontology[slot][0]
            if value != None:
                list_current_state.append(self.domain.lower()+"-"+slot+"-"+str(value))
        current_action+="\n".join(list_current_action)
        current_state +="\n".join(list_current_state)
        self.output_paper = "(TYPE) " + type + "\n\n(CURRENT ACTION)\n" + current_action + "\n\n(CURRENT STATE)\n"+ current_state

    def transform_action(self):
        self.system_action_to_response = ""
        self.output_paper = ""
        self.exist_main_slot = True
        # add old user request
        if self.dict_negate_request["request"] != {} and "asking" not in self.after_output_dst.keys() and "request":
            if "request" not in self.after_output_dst.keys():
                self.after_output_dst.setdefault("request", {})
            self.after_output_dst["request"].update(self.dict_negate_request["request"])
            self.dict_negate_request["request"] = {}

        # inform => update slots
        if "inform" in self.after_output_dst.keys():
            if self.check_req_more:
                self.check_req_more = False
            if self.check_notify_success:
                self.check_notify_success = False
            if "inform" in self.after_output_dst.keys():
                for slot, value in self.after_output_dst["inform"].items():
                    if value != self.policy.dst.slots[slot] and value != None:
                        self.change_search_slots = True
                        if slot == self.main_slot:
                            self.change_main_slot = True
                            self.exist_main_slot = self.policy.check_exist_main_slot(value)
                if self.exist_main_slot:
                    self.policy.dst.slots.update(self.after_output_dst["inform"])
                else:
                    self.change_main_slot = False

        if "request" in self.after_output_dst.keys():
            if self.only_negate_confirm:
                self.only_negate_confirm = False
        if "inform_intent" in self.after_output_dst.keys() and (self.check_req_more or self.check_notify_success):
            self.check_req_more = False
            self.check_notify_success = False

        # negate or affirm search
        if "search" in self.offer_intent.lower():
            self.negate_and_affirm_intent("search")
        # No intent == offer search
        if self.user_intent == "NONE":
            if "thank_you" not in self.after_output_dst.keys():

                # Offer intent search (if fill enough required slot search or stupid request)
                if all(self.policy.dst.slots[slot] != None for slot in self.map_intent_schema['search']) or "request" in self.after_output_dst.keys():
                    if "request" in self.after_output_dst.keys():
                        self.dict_negate_request["request"] = self.after_output_dst["request"]
                    if "inform" not in self.after_output_dst.keys() or ("inform" in self.after_output_dst.keys() and self.main_slot not in self.after_output_dst["inform"].keys()):
                        self.set_offer_intent("search")
                        self.offer_new_intent()

                if "inform" in self.after_output_dst.keys():
                    for slot, value in self.after_output_dst["inform"].items():
                        if slot in self.db_slots and slot not in self.map_intent_schema["search"] and slot != self.main_slot:
                            self.set_offer_intent("search")
                            self.offer_new_intent()
                            break
                        if self.change_main_slot:
                            self.inform_after_change_main_slot()
                            self.set_offer_intent("book")
                            self.offer_new_intent()
                            break

        # Has user intent
        else:
            # check condition intent
            result_check_intent = self.policy.check_slot(self.user_intent, self.map_intent_schema[self.user_intent])
            # Search
            if self.user_intent == "search" and ("accept" in result_check_intent or self.main_slot != ""):
                # Ony search if request_alts or no current_result or change slot in required slots
                if "request_alts" in self.after_output_dst.keys() or self.policy.current_result == {} or self.change_search_slots == True:
                    self.change_search_slots = False

                    # No input main_slot
                    if self.policy.dst.slots[self.main_slot] == None:
                        # request_alts with != old main_slot
                        alts = True if "request_alts" in self.after_output_dst.keys() or self.exist_main_slot else False
                        if self.exist_main_slot:
                            for slot in self.map_intent_schema['search']:
                                if self.policy.dst.slots[slot] != None:
                                    self.policy.search(alts)

                        if self.policy.current_result != {}:
                            self.offer_current_option()

                    # Input main_slot
                    else:
                        self.policy.search(alts = False, check_exist=True)
            # Bookif "asking" not in self.policy.output_system_action.keys()
            elif self.user_intent == "book" and "accept" in result_check_intent:
                if "affirm" in self.after_output_dst.keys():
                    if self.offer_intent != "":
                        self.policy.book(self.map_intent_schema["book"])
                        if "asking" not in self.policy.output_system_action.keys():
                            confirm_slot = self.policy.confirm_book(self.map_intent_schema["book"])
                            self.policy.output_system_action.setdefault("confirm", confirm_slot)
                            self.check_confirm = True
                    else:
                        self.policy.output_system_action.setdefault("notify_success", {"none":"none"})
                        self.check_notify_success = True
                        if "inform" not in self.policy.output_system_action.keys():
                            self.policy.output_system_action.setdefault("req_more", {"none": "none"})
                            self.check_req_more = True
                    self.check_confirm = False
                elif "negate" in self.after_output_dst.keys() or "negate_intent" in self.after_output_dst.keys():
                    if self.check_confirm == True:
                        if "thank_you" in self.after_output_dst.keys():
                            del self.after_output_dst["thank_you"]
                        if "inform" in self.after_output_dst.keys():
                            self.policy.book(self.map_intent_schema["book"])
                            if "asking" not in self.policy.output_system_action.keys():
                                confirm_slot = self.policy.confirm_book(self.map_intent_schema["book"])
                                self.policy.output_system_action.setdefault("confirm", confirm_slot)
                                self.check_confirm = True
                        else:
                            self.only_negate_confirm = True

                    elif self.check_req_more:
                        self.policy.output_system_action.update({"goodbye": {"none": "none"}})

                # move slot from dst.slots to current_book and confirm
                else:
                    self.policy.book(self.map_intent_schema["book"])
                    if "asking" not in self.policy.output_system_action.keys():
                        confirm_slot = self.policy.confirm_book(self.map_intent_schema["book"])
                        self.policy.output_system_action.setdefault("confirm", confirm_slot)
                        self.check_confirm = True

            elif self.user_intent == "get" and "accept" in result_check_intent:
                pass

            # No enough conditions
            if "accept" not in result_check_intent:
                # Book

                if self.user_intent == "book" and self.exist_main_slot:
                    result_check_search = self.policy.check_slot(self.user_intent, self.map_intent_schema["search"])
                    if "accept" in result_check_search and "select" not in self.after_output_dst.keys():

                        # no current_result or change_search_slots = True
                        if self.policy.current_result == {} or self.change_search_slots == True:
                            self.change_search_slots = False
                            if self.policy.dst.slots[self.main_slot] == None:
                                self.policy.search(alts = False)
                                self.offer_current_option()
                            else:
                                self.policy.search(alts=False, check_exist=True)
                                for s, v in self.after_output_dst["inform"].items():
                                    if v != self.policy.dst.slots[s]:
                                        if "inform" not in self.policy.output_system_action.keys():
                                            self.policy.output_system_action.setdefault("inform", {self.main_slot: self.policy.dst.slots[self.main_slot]})
                                        self.policy.output_system_action["inform"].setdefault(s, self.policy.dst.slots[s])
                                if "asking" not in self.policy.output_system_action.keys():
                                    result_check_book = self.policy.check_slot(self.user_intent, self.map_intent_schema["book"])
                                    if self.change_main_slot and self.user_intent != "book":
                                        self.set_offer_intent("book")
                                        self.offer_new_intent()

                                    else:
                                        if "inform" in self.after_output_dst.keys() and self.change_main_slot and "inform_intent" not in self.after_output_dst.keys():
                                            for slot, value in self.after_output_dst["inform"].items():
                                                self.inform_after_change_main_slot()
                                                self.set_offer_intent("book")
                                                self.offer_new_intent()
                                                break
                                        else:
                                            self.request_missing_slot(result_check_book)
                                    self.move_request_after_turn()
                        else:
                            if "asking" not in self.policy.output_system_action.keys():
                                if self.policy.current_result != {}:
                                    self.update_main_slot()
                                    if "request" not in self.after_output_dst.keys():
                                        result_check_book = self.policy.check_slot(self.user_intent, self.map_intent_schema["book"])
                                        self.request_missing_slot(result_check_book)
                                    else:
                                        self.set_offer_intent("book")
                                        self.offer_new_intent()
                                self.move_request_after_turn()
                    else:
                        if "inform" in self.after_output_dst.keys() and self.main_slot in self.after_output_dst["inform"].keys():
                            self.policy.search(alts=False, check_exist=True)
                            if "asking" not in self.policy.output_system_action.keys():
                                result_check_book = self.policy.check_slot(self.user_intent, self.map_intent_schema["book"])
                                self.request_missing_slot(result_check_book)
                                self.move_request_after_turn()
                        else:
                            if "asking" not in self.policy.output_system_action.keys():
                                if "select" in self.after_output_dst.keys():
                                    self.update_main_slot()
                                    result_check_book = self.policy.check_slot(self.user_intent, self.map_intent_schema["book"])

                                    self.request_missing_slot(result_check_book)
                                else:
                                    self.request_missing_slot(result_check_search)
                                self.move_request_after_turn()
                # Search
                elif self.user_intent == "search":
                    # TOD (not ODD)
                    if "asking" not in self.policy.output_system_action.keys() and "request" not in self.after_output_dst.keys():
                        self.request_missing_slot(result_check_intent)

            if self.policy.current_result != {} and "request" in self.after_output_dst.keys():
                if "inform" not in self.policy.output_system_action.keys():
                    self.policy.output_system_action.setdefault("inform", {})
                for slot in self.after_output_dst["request"].keys():
                    self.policy.output_system_action["inform"].update({slot: self.policy.current_result[slot]})
                    # if "notify_success" in self.policy.output_system_action.keys():
                    #     del self.policy.output_system_action["req_more"]
                self.dict_negate_request["request"] = {}

            # select == offer book
            if self.policy.current_result != {}:
                if "select" in self.after_output_dst.keys() or "affirm" in self.after_output_dst.keys() or (self.change_main_slot == True and "inform" in self.after_output_dst.keys() and self.after_output_dst["inform"][self.main_slot] == self.policy.current_result[self.main_slot]):
                    if "select" in self.after_output_dst.keys():
                        self.update_main_slot()
                    if self.change_main_slot == True:
                        self.change_main_slot = False
                    if self.user_intent == "search":
                        self.set_offer_intent("book")
                        self.offer_new_intent()

            # negate or affirm book
            for intent in self.list_action_for_intent["book"]:
                if intent in self.offer_intent.lower():
                    self.negate_and_affirm_intent("book")

        if "thank_you" in self.after_output_dst.keys():
            if "negate" in self.after_output_dst.keys() or "goodbye" in self.after_output_dst.keys():
                self.policy.output_system_action.update({"goodbye": {"none": "none"}})
            else:
                self.policy.output_system_action.update({"req_more": {"none": "none"}})
                self.check_req_more = True

        if self.check_notify_success or self.check_req_more:
            self.clear_all_things()
            if "negate" in self.after_output_dst.keys():
                self.policy.output_system_action.update({"goodbye": {"none": "none"}})

        if "goodbye" in self.after_output_dst.keys():
            self.policy.output_system_action.update({"goodbye": {"none": "none"}})

        if self.exist_main_slot == False and self.policy.current_result == {}:
            self.set_offer_intent("search")
            self.offer_new_intent()

        if self.policy.current_result == {} and self.exist_main_slot == False:
            if "request" in self.policy.output_system_action.keys():
                del self.policy.output_system_action["request"]
            self.policy.output_system_action = {}
            self.request_missing_slot([self.main_slot])

        if "offer_intent" in self.policy.output_system_action.keys():
            if "request" in self.policy.output_system_action.keys():
                del self.policy.output_system_action["request"]

        if "request" in self.policy.output_system_action.keys():
            self.requesting = True
        else:
            self.requesting = False

        for action, list_slot_value in self.policy.output_system_action.items():
            if action in ["request", "confirm"]:
                tmp = list_slot_value.copy()
                for slot, value in tmp.items():
                    if slot in self.map_ontology.keys():
                        del self.policy.output_system_action[action][slot]
                        slot = self.map_ontology[slot][0]
                        if "request" in self.policy.output_system_action.keys():
                            for des, list_slot in self.ontology.items():
                                if slot in list_slot:
                                    slot = des
                        self.policy.output_system_action[action][slot.replace("_", " ")] = value

        if "confirm" in self.policy.output_system_action.keys() and "request" in self.after_output_dst.keys():
            del self.policy.output_system_action["confirm"]
            self.set_offer_intent("book")
            self.offer_new_intent()

        if any(act in self.policy.output_system_action.keys() for act in ["notify_success", "confirm", "req_more"]):
            if "request" in self.policy.output_system_action.keys():
                del self.policy.output_system_action["request"]
        if "negate" in self.after_output_dst.keys():
            for act in ["goodbye", "request"]:
                if act in self.after_output_dst.keys():
                    del self.after_output_dst[act]

    def offer_current_option(self):
        if "inform" not in self.policy.output_system_action.keys():
            self.policy.output_system_action.setdefault("offer", {})
        for slot in self.offer_slots:
            self.policy.output_system_action["offer"].update({slot:self.policy.current_result[slot]})

    def request_missing_slot(self, list_missing):
        self.policy.output_system_action.setdefault("request", {})
        self.policy.output_system_action["request"].setdefault(random.choice(list_missing), "none")

    def set_offer_intent(self, intentStr):
        for intent in self.intent_schema.keys():
            for int in self.list_action_for_intent[intentStr]:
                if int in intent.lower():
                    self.offer_intent = intent

    def update_main_slot(self):
        self.policy.dst.update_slots({self.main_slot: self.policy.current_result[self.main_slot]})

    def negate_and_affirm_intent(self, intentStr):
        if any(act in self.after_output_dst.keys() for act in ["negate_intent", "negate"]):
            self.offer_intent = ""
            self.policy.output_system_action.setdefault("req_more", {"none": "none"})
            self.check_req_more = True
        if any(act in self.after_output_dst.keys() for act in ["affirm_intent", "affirm", "select"]):
            self.user_intent = intentStr
            if intentStr == "book":
                self.offer_intent = ""
                if "asking" not in self.policy.output_system_action.keys():
                    result_check_book = self.policy.check_slot(self.user_intent, self.map_intent_schema["book"])
                    self.request_missing_slot(result_check_book)

    def offer_new_intent(self):
        if self.offer_intent != "":
            self.policy.output_system_action.setdefault("offer_intent", {"intent": self.offer_intent})

    def move_request_after_turn(self):
        if "request" in self.after_output_dst.keys():
            self.dict_negate_request["request"] = self.after_output_dst["request"]

    def inform_after_change_main_slot(self):
        self.change_main_slot = False
        self.policy.search(alts=False, check_exist=True)
        for s, v in self.after_output_dst["inform"].items():
            if v != self.policy.dst.slots[s]:
                if "inform" not in self.policy.output_system_action.keys():
                    self.policy.output_system_action.setdefault("inform", {
                        self.main_slot: self.policy.dst.slots[self.main_slot]})
                self.policy.output_system_action["inform"].setdefault(s, self.policy.dst.slots[s])

    def clear_all_things(self):
        self.change_search_slots = False
        self.change_main_slot = False
        self.check_confirm = False
        self.user_intent = "NONE"
        self.offer_intent = ""
        self.output_system_action = {}
        self.dict_negate_request = {"request": {}}
        self.policy.dst.reset_slots(self.policy.map_ontology)
        self.policy.count_search = 0
        self.policy.current_result = {}
        self.policy.current_book = {}
        self.change_slots_after_negate = {}
        self.previous_main_slot = {self.main_slot: []}