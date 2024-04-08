import sqlite3

def check_missing_slots(current_slots, required_slots):
    missing_slots = []
    for slot in required_slots:
        if current_slots[slot] is None:
            missing_slots.append(slot)
    return missing_slots

def generate_query_check_exist_main_slot(domain, main_slot, new_value):
    new_value = "'{}'".format(new_value) if type(new_value) == str else new_value
    condition = f"{main_slot} = {new_value}"
    query = "SELECT * FROM " + domain + " WHERE " + condition
    return query

def generate_query_search(dict_to_search, previous_main_slot, domain, current_result = {}):
    query = "SELECT * FROM "+domain+" WHERE "
    conditions = []
    for slot, value in dict_to_search.items():
        value = "'{}'".format(value) if type(value) == str else value
        condition = f"{slot} = {value}"
        conditions.append(condition)

    if current_result != {}:
        for value in list(previous_main_slot.values())[0]:
            slot = list(previous_main_slot.keys())[0]
            condition = f"{slot} != '{value}'"
            conditions.append(condition)
    query += " AND ".join(conditions)
    # print("---query: ", query)
    return query

def select_db(query, path_db):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows