import sqlite3
conn = sqlite3.connect(r'C:\ALL\FPT\AIP\aip_final\src\module_action\db_hotels_2\hotels_2.db')
cursor = conn.cursor()

drop_table_query = "DROP TABLE HOTELS_2"
cursor.execute(drop_table_query)

create_table_query = '''
CREATE TABLE HOTELS_2 (
    slot0 TEXT,
    slot4 INTEGER,
    slot5 TEXT PRIMARY KEY,
    slot6 TEXT,
    slot7 INTEGER,
    slot8 TEXT,
    number_of_rooms_available INTEGER
);
'''
cursor.execute(create_table_query)
conn.commit()
conn.close()