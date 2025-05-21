#THIS IS TO KNOW THE ADMINSTRATOR DATAS
import sqlite3

Choice = int(input("1- Passenger, 2- Adminstrator, " + "\n1"))

if Choice == 1:

    connection = sqlite3.connect("project_data.db")
    cursor = connection.cursor()
    cursor.execute("SELECT *, oid FROM Passenger")
    rows = cursor.fetchall()

    # Print each row
    for row in rows:
        print(row)

elif Choice == 2:

    connection = sqlite3.connect("project_data.db")
    cursor = connection.cursor()
    cursor.execute("SELECT *, oid FROM Administrator")
    rows = cursor.fetchall()

    # Print each row
    for row in rows:
        print(row)
