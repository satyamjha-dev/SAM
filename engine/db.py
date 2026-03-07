import os
import sqlite3

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, '..', 'sam.db')
db_path = os.path.abspath(db_path)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

query = "CREATE TABLE IF NOT EXISTS sys_command (id INTEGER PRIMARY KEY, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)

cursor.execute("INSERT INTO sys_command VALUES (NULL, 'whatsapp', '/Applications/WhatsApp.app')")
cursor.execute("INSERT INTO sys_command VALUES (NULL, 'chrome', '/Applications/Google Chrome.app')")
cursor.execute("INSERT INTO sys_command VALUES (NULL, 'brave', '/Applications/Brave Browser.app')")
cursor.execute("INSERT INTO sys_command VALUES (NULL, 'safari', '/Applications/Safari.app')")
cursor.execute("INSERT INTO sys_command VALUES (NULL, 'vscode', '/Applications/Visual Studio Code.app')")
cursor.execute("INSERT INTO sys_command VALUES (NULL, 'terminal', '/System/Applications/Utilities/Terminal.app')")

conn.commit()

