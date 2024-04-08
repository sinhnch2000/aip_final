
from abc import ABC, abstractmethod
from DST import DialogueStateTracker
from utils import *
import sqlite3


class Policy(ABC):
    def __init__(self, map_ontology, main_slot, db_slots, path_db, domain):
        self.count_search = 0
        self.current_result = {}
        self.path_db = path_db
        self.current_book = {}
        self.domain = domain
        self.change_slots_after_negate = {}
        self.map_ontology = map_ontology
        self.main_slot = main_slot
        self.previous_main_slot = {self.main_slot: []}
        self.db_slots = db_slots
        self.output_system_action = {}
        self.dst = DialogueStateTracker(self.map_ontology)

    def check_slot(self, intent, required_slots):
        list_missing_required_slots = check_missing_slots(self.dst.slots, required_slots)
        if len(list_missing_required_slots) == 0:
            return "accept_" + intent
        else:
            return list_missing_required_slots

    def check_exist_main_slot(self, new_value):
        query = generate_query_check_exist_main_slot(self.domain, self.main_slot, new_value)
        rows = select_db(query, self.path_db)
        if rows:
            tmp = {}
            for i in range(len(self.db_slots)):
                tmp.setdefault(self.db_slots[i], rows[0][i])
            for result_slot, result_value in tmp.items():
                self.dst.slots[result_slot] = result_value
            return True
        else:
            return False

    def search(self, alts, check_exist=False):
        dict_slots_to_search = {}
        tmp = {}
        if check_exist:
            for slotdigit, value in self.dst.slots.items():
                if slotdigit == self.main_slot:
                    tmp.setdefault(slotdigit, value)
                else:
                    tmp.setdefault(slotdigit, None)
            for slot, value in tmp.items():
                if value != None and slot in self.db_slots:
                    dict_slots_to_search.setdefault(slot, value)
        else:
            for slot, value in self.dst.slots.items():
                if value != None and slot in self.db_slots:
                    dict_slots_to_search.setdefault(slot, value)
        query = generate_query_search(dict_slots_to_search, self.previous_main_slot, self.domain, self.current_result) if alts else generate_query_search(dict_slots_to_search, self.previous_main_slot, self.domain)
        rows = select_db(query, self.path_db)
        if rows:
            self.current_result.clear()
            for i in range(len(self.db_slots)):
                self.current_result.setdefault(self.db_slots[i], rows[0][i])
            self.count_search = len(rows)
            # print("---result:", self.current_result, "\n")
            if self.current_result[self.main_slot] not in self.previous_main_slot[self.main_slot]:
                self.previous_main_slot[self.main_slot].append(self.current_result[self.main_slot])
            if check_exist:
                for result_slot, result_value in self.current_result.items():
                    self.dst.slots[result_slot] = result_value

    def book(self, required_slots):
        for slot in self.db_slots:
            if "slot" in slot:
                self.current_book[slot] = self.current_result[slot]
        for slot in required_slots:
            if self.dst.slots[slot] != None:
                self.current_book[slot] = self.dst.slots[slot]

    def get(self, slots_values_requested):
        if self.current_result == {}:
            dict_to_search = {"hotel_name": self.tracker.slots["hotel_name"]}
            query = generate_query(dict_to_search)
            rows = select_db(query)
            if rows:
                for i in range(len(self.db_slots)):
                    self.current_result.setdefault(self.db_slots[i], rows[0][i])
                # print("---result:", self.current_result)

        inform_value = {}
        for i in slots_values_requested:
            slot = i
            inform_value.setdefault(slot, self.current_result[i])
        return inform_value

    def confirm_book(self, required_slots):
        confirm_slot = {}
        if self.change_slots_after_negate != {}:
            confirm_slot.update(self.change_slots_after_negate)
            self.change_slots_after_negate.clear()
        else:
            for slot in required_slots:
                confirm_slot.setdefault(slot, self.convert_str_to_int(self.current_book[slot]))

        return confirm_slot

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
            int(string)
            return int(string)
        except ValueError:
            pass

        string = string.strip()
        for str, i in english_to_number_dict.items():
            if string.lower() == str:
                return int(i)
        return string