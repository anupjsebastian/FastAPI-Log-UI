import sqlite3

def print_all_records(db_path):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM logs")
        records = cursor.fetchall()
        for record in records:
            print(record)




print_all_records("nas_dir/service.db")