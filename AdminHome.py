from tkinter import *
import subprocess
from tkinter import messagebox
import sqlite3
root = Tk()
root.title("Airplan Reservation System Project/AdminHome")

all_widgets = []
#root.geometry("800x600")
#root.grid_columnconfigure(0, weight=1)
#root.grid_columnconfigure(1, weight=2)
#root.grid_rowconfigure(0, weight=1)

###########################################
###########################################
###########################################
###########################################

def FlightSection():
    global FlightWin, Flightframe
    FlightWin = Toplevel()
    FlightWin.geometry("1200x600")
    FlightWin.title("Airplane Reservation System Project/AdminHome/FlightSection")
    Flightframe = LabelFrame(FlightWin, padx=25, pady=75, bg="#d2cfcf")
    Flightframe.grid(row=0, column=0)

    showButFlight = Button(Flightframe, text="Show Flights", width=15, command=showFlight, bd=1)
    showButFlight.grid(row=0, column=0, padx=(10, 50), pady=(50, 10))

    upButFlight = Button(Flightframe, text="Update Flight", width=15, command=updateflight, bd=1)
    upButFlight.grid(row=1, column=0, padx=(10, 50), pady=(10, 10), sticky=W)

    exitFlight = Button(Flightframe, text=" Exit", width=15, command=FlightWin.destroy, bd=1)
    exitFlight.grid(row=3, column=0, padx=(10, 50), pady=(10, 10), sticky=W)


def save_updated_flight_info():
    global flight_id, airline, source, destination, departure, arrival, capacity, seats, price, entryFlightId
    global current_flight_id_key  # <-- ADD THIS LINE

    connect = sqlite3.connect("project_data.db")
    cursor = connect.cursor()

    cursor.execute("""
    UPDATE Flight SET
        airline = ?,
        source = ?,
        destination = ?,
        departure_time = ?,
        arrival_time = ?,
        capacity = ?,
        available_seats = ?,
        base_price = ?
    WHERE flight_id = ?
    """,
    (
        airline.get(),
        source.get(),
        destination.get(),
        departure.get(),
        arrival.get(),
        capacity.get(),
        seats.get(),
        price.get(),
        current_flight_id_key
    ))

    connect.commit()
    connect.close()

    # Clear fields
    fields = [flight_id, airline, source, destination, departure, arrival, capacity, seats, price, entryFlightId]
    for field in fields:
        field.delete(0, END)

    messagebox.showinfo("Success", "Flight data updated successfully!")
    

def updateflight2(f_id):
    global flight_id, airline, source, destination, departure, arrival, capacity, seats, price
    global frameR, entryFlightId, update_flight_button, current_flight_id_key, all_widgets

    current_flight_id_key = f_id

    try:
        f_id = str(f_id)
    except ValueError:
        messagebox.showerror("Invalid ID", "Please enter a valid Flight ID.")
        return

    # Create entries
    labels = ["Flight ID", "Airline", "Source", "Destination", "Departure", "Arrival", "Capacity", "Available Seats", "Base Price"]
    entries = []

    for i, text in enumerate(labels):
        Label(frameR, text=text).grid(row=i + 1, column=0, pady=(5, 5))
        entry = Entry(frameR, width=50)
        entry.grid(row=i + 1, column=1, pady=(5, 5))
        entries.append(entry)

    flight_id, airline, source, destination, departure, arrival, capacity, seats, price = entries

    # Fetch and populate data
    connect = sqlite3.connect("project_data.db")
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM Flight WHERE flight_id = ?", (f_id,))
    data = cursor.fetchone()

    if data:
        for i, value in enumerate(data):
            entries[i].insert(0, value)
    else:
        messagebox.showerror("Not Found", "No flight found with that ID.")
        return

    connect.close()

    update_flight_button = Button(frameR, text="Update2", command=save_updated_flight_info)
    update_flight_button.grid(row=10, column=0, columnspan=2, pady=(10, 5))

    all_widgets += entries + [update_flight_button]


def updateflight():
    global all_widgets
    global frameR, labelFlightId, entryFlightId, confirmFlight

    for widget in all_widgets:
        widget.destroy()
    all_widgets = []

    frameR = LabelFrame(FlightWin, text="Update Flight")
    frameR.grid(row=0, column=1, padx=10, pady=10, sticky=E)

    labelFlightId = Label(frameR, text="Enter Flight ID to update:")
    labelFlightId.grid(row=0, column=0, sticky=E)

    entryFlightId = Entry(frameR)
    entryFlightId.grid(row=0, column=1, sticky=W)

    confirmFlight = Button(frameR, text="Update1", command=lambda: updateflight2(entryFlightId.get()))
    confirmFlight.grid(row=0, column=2, padx=5)

    all_widgets += [frameR, labelFlightId, entryFlightId, confirmFlight]


def showFlight():
    global all_widgets
    global frameR, Layout

    for widget in all_widgets:
        widget.destroy()
    all_widgets = []

    frameR = LabelFrame(FlightWin, text="Show Flights")
    frameR.grid(row=0, column=1, padx=10, pady=10, sticky=E)

    connection = sqlite3.connect("project_data.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Flight")
    rows = cursor.fetchall()

    Layout = Label(frameR, text="1Flight ID | 2Airline | 3Source | 4Destination | 5Departure | 6Arrival | 7Capacity | 8Available | 9Price")
    Layout.grid(row=0, column=1)

    for i, row in enumerate(rows):
        Data = Label(frameR, text=str(row) + ",")
        Data.grid(row=i + 1, column=1, sticky='w')

    all_widgets += [frameR, Layout]






###########################################
###########################################
###########################################
###########################################
def PassengerSection():

    global PassWin, Passframe
    PassWin = Toplevel()
    PassWin.geometry("1200x600")
    PassWin.title("Airplan Reservation System Project/AdminHome/PassengerSection")
    Passframe = LabelFrame(PassWin, padx = 25, pady = 75, bg = "#d2cfcf")
    Passframe.grid(row = 0, column = 0)

    showButPass = Button(Passframe, text = "Show Data", width = 15, command = showPass, bd = 1)
    showButPass.grid(row = 0, column = 0, padx = (10, 50), pady = (50, 10))

    upButPass = Button(Passframe, text = "Update Data", width = 15, command = updatepass, bd = 1)
    upButPass.grid(row = 1, column = 0, padx = (10, 50), pady = (10, 10), sticky = W)

    delButPass = Button(Passframe, text = "Delete Data", width = 15, command = deletepass, bd = 1)
    delButPass.grid(row = 2, column = 0, padx = (10, 50), pady = (10, 10), sticky = W)

    exitPass = Button(Passframe, text = " Exit", width = 15, command = PassWin.destroy, bd = 1)
    exitPass.grid(row = 3, column = 0, padx = (10, 50), pady = (10, 10), sticky = W)

###########################################

def deletepass2():

    global entryId
    global all_widgets
    
    try:
        key = int(entryId.get())
    except ValueError:
        messagebox.showerror("Invalid ID", "Please enter a valid numeric ID.")
        return

    answer = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete Passenger with ID {key}?")

    if answer:
        messagebox.showinfo("Deleted", f"Passenger with ID {key} has been deleted.")
        entryId.delete(0, END)  # Clear the entry box

        connect = sqlite3.connect("project_data.db")
        cursor = connect.cursor()
        cursor.execute("DELETE FROM Passenger WHERE passenger_id = ?", (key,))
            
        connect.commit()
        connect.close()
    
    
    else:
        messagebox.showinfo("Cancelled", "Deletion cancelled.")

    


###########################################

def deletepass():
    
    global all_widgets
    global entryId, labelId, frameR, confirm

    for widget in all_widgets:
        widget.destroy()
    all_widgets = []

    frameR = LabelFrame(PassWin, text="Delete")
    frameR.grid(row=0, column=1, padx=10, pady=10, sticky=E)

    labelId = Label(frameR, text="Enter ID to delete:")
    labelId.grid(row=0, column=0, sticky=E)

    entryId = Entry(frameR)
    entryId.grid(row=0, column=1, sticky=W)

    confirm = Button(frameR, text="Delete", command = deletepass2)
    confirm.grid(row=0, column=2, padx=5)

    all_widgets += [frameR, labelId, entryId, confirm]


###########################################
###########################################
def save_updated_info():

    global usernamePass, emailPass, passwordPass, contactPass, idPass, age, gender, passportNum, frequentFly, entryId

    connect = sqlite3.connect("project_data.db")
    cursor = connect.cursor()

    cursor.execute("""
    UPDATE Passenger SET
        user_name = ?,
        email = ?,
        password = ?,
        contact_number = ?,
        passenger_id = ?,
        age = ?,
        gender = ?,
        passport_number = ?,
        frequent_flyer_status = ?
    WHERE passenger_id = ?
""", 
(
        usernamePass.get(),
        emailPass.get(),
        passwordPass.get(),
        contactPass.get(),
        idPass.get(),
        age.get(),
        gender.get(),
        passportNum.get(),
        frequentFly.get(),
        current_id_key
    ))

    connect.commit()
    connect.close()

    entryId.delete(0, END)
    usernamePass.delete(0, END)
    emailPass.delete(0, END)
    passwordPass.delete(0, END)
    contactPass.delete(0, END)
    idPass.delete(0, END)
    age.delete(0, END)
    gender.delete(0, END)
    passportNum.delete(0, END)
    frequentFly.delete(0, END)



    messagebox.showinfo("Success", "Passenger data updated successfully!")


###########################################

def updatepass2(key):
    global label1, label2, label3, label4, label5, label6, label7, label8, label9
    global usernamePass, emailPass, passwordPass, contactPass, idPass, age, gender, passportNum, frequentFly
    global all_widgets, frameR, entryId, update_button, current_id_key

    current_id_key = key  # Store the key for use in update2

    try:
        key = str(key)
    except ValueError:
        messagebox.showerror("Invalid ID", "Please enter a valid numeric ID.")
        return
    


    # Create all the labels and entries
    label1 = Label(frameR, text="UserName")
    label1.grid(row=1, column=0, pady=(5, 5))
    usernamePass = Entry(frameR, width=50)
    usernamePass.grid(row=1, column=1, pady=(5, 5))

    label2 = Label(frameR, text="Email")
    label2.grid(row=2, column=0, pady=(5, 5))
    emailPass = Entry(frameR, width=50)
    emailPass.grid(row=2, column=1, pady=(5, 5))

    label3 = Label(frameR, text="Password")
    label3.grid(row=3, column=0, pady=(5, 5))
    passwordPass = Entry(frameR, width=50)
    passwordPass.grid(row=3, column=1, pady=(5, 5))

    label4 = Label(frameR, text="Contact Number")
    label4.grid(row=4, column=0, pady=(5, 5))
    contactPass = Entry(frameR, width=50)
    contactPass.grid(row=4, column=1, pady=(5, 5))

    label5 = Label(frameR, text="National ID")
    label5.grid(row=5, column=0, pady=(5, 5))
    idPass = Entry(frameR, width=50)
    idPass.grid(row=5, column=1, pady=(5, 5))

    label6 = Label(frameR, text="Age")
    label6.grid(row=6, column=0, pady=(5, 5))
    age = Entry(frameR, width=50)
    age.grid(row=6, column=1, pady=(5, 5))

    label7 = Label(frameR, text="Gender")
    label7.grid(row=7, column=0, pady=(5, 5))
    gender = Entry(frameR, width=50)
    gender.grid(row=7, column=1, pady=(5, 5))

    label8 = Label(frameR, text="Passport Number")
    label8.grid(row=8, column=0, pady=(5, 5))
    passportNum = Entry(frameR, width=50)
    passportNum.grid(row=8, column=1, pady=(5, 5))

    label9 = Label(frameR, text="Frequent Flyer")
    label9.grid(row=9, column=0, pady=(5, 5))
    frequentFly = Entry(frameR, width=50)
    frequentFly.grid(row=9, column=1, pady=(5, 5))

    # Populate data from database
    connect = sqlite3.connect("project_data.db")
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM Passenger WHERE passenger_id = " + (key))
    data = cursor.fetchone()

    if data:
        usernamePass.insert(0, data[0])
        emailPass.insert(0, data[1])
        passwordPass.insert(0, data[2])
        contactPass.insert(0, data[3])
        idPass.insert(0, data[4])
        age.insert(0, data[5])
        gender.insert(0, data[6])
        passportNum.insert(0, data[7])
        frequentFly.insert(0, data[8])

    else:
        messagebox.showerror("Not Found", "No record found with that ID.")
        return

    connect.commit()
    connect.close()

    # Add Update2 button
    update_button = Button(frameR, text="Update2", command= save_updated_info)
    update_button.grid(row=10, column=0, columnspan=2, pady=(10, 5))
    
    all_widgets += [
        usernamePass, emailPass, passwordPass, contactPass, idPass, age,
        gender, passportNum, frequentFly, label1, label2, label3, label4,
        label5, label6, label7, label8, label9, update_button
    ]


def updatepass():
    global all_widgets
    global frameR, labelId, entryId, confirm

    for widget in all_widgets:
        widget.destroy()
    all_widgets = []

    frameR = LabelFrame(PassWin, text="Update")
    frameR.grid(row=0, column=1, padx=10, pady=10, sticky=E)

    labelId = Label(frameR, text="Enter ID to update:")
    labelId.grid(row=0, column=0, sticky=E)

    entryId = Entry(frameR)
    entryId.grid(row=0, column=1, sticky=W)

    confirm = Button(frameR, text="Update1", command= lambda: updatepass2(int(entryId.get())))
    confirm.grid(row=0, column=2, padx=5)

    all_widgets += [frameR, labelId, entryId, confirm]


##########################################
###########################################
 
def showPass():
    
    #to destroy all widgets with changed button
    global all_widgets
    global Data, frameR, Layout

    for widget in all_widgets:
        widget.destroy()
    all_widgets = []

    frameR = LabelFrame(PassWin, text = "Show")
    frameR.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = E)
    
    connection = sqlite3.connect("project_data.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Passenger")
    rows = cursor.fetchall()

    Layout = Label(frameR, text = "1Username | 2Email | 3Password | 4Contact | 5Passenger ID | 6Age | 7Gender | 8Passport | 9FrequentFlyer")
    Layout.grid(row = 0, column = 1)
    # Print each row
    for i, row in enumerate(rows):  
        Data = Label(frameR, text= str(row) + ",")
        Data.grid(row=i+1, column=1, sticky='w')

    all_widgets += [Data, Layout, frameR]
        

    

###########################################
###########################################
###########################################
###########################################    

def logout():
    root.quit()
    subprocess.Popen(["python", "Airline-reservation-system\Log_in&Sign_up.py"])

###########################################
###########################################    


frameL = LabelFrame(root, text = "Home Sweet Home!!", padx = 100, pady = 300, bg = "#d2cfcf")
frameL.grid(row = 0, column = 0,padx = 10, pady = 10)

##
button1 = Button(frameL, text = "Passenger Section", width = 50, command = PassengerSection, bd = 1)
button1.grid(row = 1, column = 0, padx = 10, pady = 10)

button2 = Button(frameL, text = "Flights Section",width = 50, command = FlightSection, bd = 1)
button2.grid(row = 2, column = 0, padx = 10, pady = 10)

button3 = Button(frameL, text = "Contact Support(coming soon)", width = 50, command = None, bd = 1)
button3.grid(row = 3, column = 0, padx = 10, pady = 10)

button4 = Button(frameL, text = "Payments Section(coming soon)", width = 50, command = None, bd = 1)
button4.grid(row = 4, column = 0, padx = 10, pady = 10)

button5 = Button(frameL, text = "LogOut", width = 50, command = logout, bd = 1)
button5.grid(row = 5, column = 0, padx = 10, pady = 10)

buttonbox = Button(frameL, text = "🙂", command = root.quit)
buttonbox.grid(row = 6, column = 1, sticky = SE)





root.mainloop()