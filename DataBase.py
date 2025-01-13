import sqlite3

DATABASE_NAME = "game_data.db"

def create_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_times (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time_played INTEGER
        )
    """)
    conn.commit()
    conn.close()

def add_time(time):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO game_times (time_played) VALUES (?)", (time,))
    conn.commit()
    conn.close()

def get_total_time():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(time_played) FROM game_times")
    total_time = cursor.fetchone()[0]
    conn.close()
    return total_time if total_time else 0

# Создаем базу данных при запуске
create_database()