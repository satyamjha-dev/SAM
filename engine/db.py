import csv
import os
import sqlite3

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, '..', 'sam.db')
db_path = os.path.abspath(db_path)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

query = "CREATE TABLE IF NOT EXISTS sys_command (id INTEGER PRIMARY KEY, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)

cursor.execute('''
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY,
    name TEXT,
    mobile_no TEXT,
    email TEXT
)
''')

cursor.execute("INSERT INTO sys_command VALUES (NULL, 'whatsapp', '/Applications/WhatsApp.app')")
cursor.execute("INSERT INTO sys_command VALUES (NULL, 'chrome', '/Applications/Google Chrome.app')")
cursor.execute("INSERT INTO sys_command VALUES (NULL, 'brave', '/Applications/Brave Browser.app')")
cursor.execute("INSERT INTO sys_command VALUES (NULL, 'safari', '/Applications/Safari.app')")
cursor.execute("INSERT INTO sys_command VALUES (NULL, 'vscode', '/Applications/Visual Studio Code.app')")
cursor.execute("INSERT INTO sys_command VALUES (NULL, 'terminal', '/System/Applications/Utilities/Terminal.app')")

conn.commit()


# Read data from CSV and insert into SQLite table for the desired columns
desired_columns_indices = [0, 18]

with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)

    for row in csvreader:
        selected_data = [row[i] for i in desired_columns_indices]

        cursor.execute(
            "INSERT INTO contacts (name, mobile_no) VALUES (?, ?)",
            tuple(selected_data)
        )

# Commit changes and close connection
conn.commit()
conn.close()
