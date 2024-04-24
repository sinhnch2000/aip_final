import sqlite3

conn = sqlite3.connect(r'C:\ALL\FPT\AIP\aip_final\src\module_action\db_hotels_1\hotels_1.db')
cursor = conn.cursor()

insert_query = """
INSERT INTO HOTELS_1 (slot0, 
                      slot4, 
                      slot5,
                      slot6,
                      slot7,
                      slot8,
                      slot9) VALUES (?, ?, ?, ?, ?, ?, ?)"""

hotel_1_data = [
    ("District 1", 4, 'CayXanh', "21 Nguyen Hue", "0903610477", 12, "True"),
    ("District 1", 5, 'CayHong', "13 Dong Khoi", "0822610477", 20, "True"),
    ("District 3", 3, 'CayVang', "23 Nguyen Xien", "0972334567", 8, "True"),
    ("District 1", 4, 'CayDen', "134 CMT8", "0972334567", 7, "True"),
    ("District 1", 5, 'CayDo', "15 Pham Dang Giang", "0972334567", 7, "True"),
]

cursor.executemany(insert_query, hotel_1_data)

conn.commit()
conn.close()