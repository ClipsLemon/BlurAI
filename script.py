import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('blurAI.db')
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Photo (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    processed INTEGER DEFAULT 0,
	way_name TEXT NOT NULL
);
''')

connection.commit()
connection.close()

