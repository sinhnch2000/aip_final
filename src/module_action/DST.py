class DialogueStateTracker:
    def __init__(self, map_ontology):
        self.reset_slots(map_ontology)
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

    def update_slots(self, slots_values):
        for slot, value in slots_values.items():
            value = self.convert_str_to_int(value)
            if "slot" in slot:
                self.slots[slot] = value