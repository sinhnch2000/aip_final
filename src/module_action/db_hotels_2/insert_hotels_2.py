import sqlite3

conn = sqlite3.connect(r'C:\ALL\FPT\AIP\aip_final\src\module_action\db_hotels_2\hotels_2.db')
cursor = conn.cursor()

insert_query = """
INSERT INTO HOTELS_2 (slot0, 
                      slot4, 
                      slot5,
                      slot6,
                      slot7,
                      slot8,
                      number_of_rooms_available) VALUES (?, ?, ?, ?, ?, ?, ?)"""

hotel_2_data = [
    ("District 1", 4, "21 Nguyen Hue", "0903610477", 12, "True", 23),
    ("District 1", 5, "13 Dong Khoi", "0822610477", 20, "False", 1),
    ("District 3", 3, "23 Nguyen Xien", "0972334567", 8, "True", 2),
    ("District 1", 4, "134 CMT8", "0972334567", 7, "True", 2),
]

cursor.executemany(insert_query, hotel_2_data)

conn.commit()
conn.close()