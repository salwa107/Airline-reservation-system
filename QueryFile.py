#THIS IS TO KNOW THE ADMINSTRATOR DATAS
import sqlite3

connection = sqlite3.connect("project_data.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM Administrator")
rows = cursor.fetchall()

# Print each row
for row in rows:
    print(row)