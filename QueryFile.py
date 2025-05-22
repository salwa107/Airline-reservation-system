#THIS IS TO KNOW THE ADMINSTRATOR DATAS
import sqlite3

Choice = int(input("1- Passengertable, 2-PassengerData , 3- Adminstrator, 4- Flights" + "\n"))

if Choice == 1:

    conn = sqlite3.connect("project_data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='Passenger'")
    print(cursor.fetchone()[0])


elif Choice == 2:
    conn = sqlite3.connect("project_data.db")
    cursor = conn.cursor()
    rows = cursor.fetchall()

    for row in rows:
        print(row)

elif Choice == 3:

    connection = sqlite3.connect("project_data.db")
    cursor = connection.cursor()
    cursor.execute("SELECT *, oid FROM Administrator")
    rows = cursor.fetchall()

    # Print each row
    for row in rows:
        print(row)

elif Choice == 4:

    connection = sqlite3.connect("project_data.db")
    cursor = connection.cursor()
    cursor.execute("SELECT *, oid FROM Flight")
    rows = cursor.fetchall()

    # Print each row
    for row in rows:
        print(row)
