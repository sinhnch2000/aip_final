import sqlite3
conn = sqlite3.connect(r'C:\ALL\FPT\AIP\aip_final\src\module_action\db_restaurants_1\restaurants_1.db')
cursor = conn.cursor()

drop_table_query = "DROP TABLE RESTAURANTS_1"
cursor.execute(drop_table_query)

create_table_query = '''
CREATE TABLE RESTAURANTS_1 (
    slot0 TEXT PRIMARY KEY,
    slot3 TEXT,
    slot4 TEXT,
    slot5 TEXT,
    slot6 TEXT,
    slot8 TEXT,
    slot9 TEXT,
    slot10 TEXT,
    number_of_tables_available INTEGER
);
'''
cursor.execute(create_table_query)
conn.commit()
conn.close()