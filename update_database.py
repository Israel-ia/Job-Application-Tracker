import sqlite3

connection = sqlite3.connect("applications.db")

cursor = connection.cursor()

cursor.execute(
    """
    ALTER TABLE applications
    ADD COLUMN notes TEXT
    """
)

connection.commit()
connection.close()

print("Notes column added.")