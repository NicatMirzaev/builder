import sqlite3 as sql

connection = sql.connect("objects.db", check_same_thread=False)
cursor = connection.cursor()

def load_database():
    cursor.execute("CREATE TABLE IF NOT EXISTS objects (id INTEGER PRIMARY KEY AUTOINCREMENT, object_name TEXT, x INTEGER, y INTEGER, rotation INTEGER)")
    connection.commit()

def add_object(name, x, y):
    cursor.execute("INSERT INTO objects (object_name, x, y, rotation) VALUES (?, ?, ?, ?)", (name, x, y, 0))
    connection.commit()
    return cursor.lastrowid

def delete_object(id):
    cursor.execute("DELETE FROM objects WHERE id=?", (id,))
    connection.commit()

def update_rotation(id, rotation):
    cursor.execute("UPDATE objects SET rotation=? WHERE id=?", (rotation, id))
    connection.commit()

def get_objects():
    cursor.execute("SELECT * FROM objects")
    data = cursor.fetchall()
    return data
