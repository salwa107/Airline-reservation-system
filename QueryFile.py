#THIS IS TO KNOW THE ADMINSTRATOR DATAS
import sqlite3

Choice = int(input("1- Passengertable, 2-PassengerData , 3- Adminstrator, 4- Add Flights, 5- Show Flights" + "\n"))

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

    conn = sqlite3.connect("project_data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print("Tables in database:", tables)
    conn.close()

    flight_id = input("Enter Flight ID: ")
    airline = input("Enter Airline: ")
    source = input("Enter Source: ")
    destination = input("Enter Destination: ")
    departure_time = input("Enter Departure Time (e.g. 14:30): ")
    arrival_time = input("Enter Arrival Time (e.g. 18:45): ")
    capacity = int(input("Enter Capacity: "))
    available_seats = int(input("Enter Available Seats: "))
    base_price = float(input("Enter Base Price: "))

    try:
            connection = sqlite3.connect("project_data.db")
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO Flight (
                    flight_id, airline, source, destination,
                    departure_time, arrival_time, capacity,
                    available_seats, base_price
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                flight_id, airline, source, destination,
                departure_time, arrival_time, capacity,
                available_seats, base_price
            ))
            connection.commit()

            connection.close()
            print("Flight added successfully!")
    except sqlite3.IntegrityError:
            print("Error: Flight ID already exists.")
    except Exception as e:
            print("An error occurred:", e)



elif Choice == 5:

    connection = sqlite3.connect("project_data.db")
    cursor = connection.cursor()
    cursor.execute("SELECT *, oid FROM Flight")
    rows = cursor.fetchall()

    # Print each row
    for row in rows:
        print(row)

