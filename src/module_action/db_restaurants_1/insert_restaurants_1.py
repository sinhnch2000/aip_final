import sqlite3

conn = sqlite3.connect(r'C:\ALL\FPT\AIP\aip_final\src\module_action\db_restaurants_1\restaurants_1.db')
cursor = conn.cursor()

insert_query = """
INSERT INTO RESTAURANTS_1 (slot0, 
                           slot3,
                           slot4, 
                           slot5,
                           slot6,
                           slot8,
                           slot9,
                           slot10,
                           number_of_tables_available) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""

restaurants_1_data = [
    ("CayXanh", "True", "True", "0903610477", "21 Nguyen Hue", "moderate", "HoChiMinh", "French", 5),
    ("CayDen", "False", "False", "0822610477", "13 Dong Khoi", "moderate", "DaNang", "VietNam", 7),
    ("CayVang", "False", "True", "0972334567", "23 Nguyen Xien", "moderate", "HaNoi", "Chinese", 8),
    ("CayHong", "True", "True", "0972334567", "134 CMT8", "moderate", "HoChiMinh", "Brasserie", 9),
]

cursor.executemany(insert_query, restaurants_1_data)

conn.commit()
conn.close()