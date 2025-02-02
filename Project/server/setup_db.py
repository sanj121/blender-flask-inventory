import sqlite3

# Create a connection to the database (it will create the file if it doesn't exist)
conn = sqlite3.connect('../database/inventory.db')
cursor = conn.cursor()

# Create an inventory table if it doesn't already exist
cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    quantity INTEGER NOT NULL)''')

# Commit and close the connection
conn.commit()
conn.close()

print("Database setup complete!")

