import sqlite3
conn = sqlite3.connect(r'C:\ALL\FPT\AIP\aip_final\src\module_action\db_hotels_1\hotels_1.db')
cursor = conn.cursor()

drop_table_query = "DROP TABLE HOTELS_1"
cursor.execute(drop_table_query)

create_table_query = '''
CREATE TABLE HOTELS_1 (
    slot0 TEXT,
    slot4 INTEGER,
    slot5 TEXT PRIMARY KEY,
    slot6 TEXT,
    slot7 TEXT,
    slot8 INTEGER,
    slot9 TEXT);
'''
cursor.execute(create_table_query)
conn.commit()
conn.close()