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



#f

#HOW TO ADD TWO FRAMES BESIDE EACH OTHER IN ONE FRAME????
#HOW TO SEND THE INFORMATION FROM THE LOGIN TO THE ADMIN FILE AND TO PASSENGER FILE

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

    delButPass = Button(Passframe, text = "Delete Data", width = 15, command = None, bd = 1)
    delButPass.grid(row = 2, column = 0, padx = (10, 50), pady = (10, 10), sticky = W)

    exitPass = Button(Passframe, text = " Exit", width = 15, command = PassWin.destroy, bd = 1)
    exitPass.grid(row = 3, column = 0, padx = (10, 50), pady = (10, 10), sticky = W)

###########################################

def updatepass2(key):
    global label1, label2, label3, label4, label5, label6, label7, label8, label9
    global usernamePass, emailPass, passwordPass, contactPass, idPass, age, gender, passportNum, frequentFly
    global frameR, entryId

    #try:
    #    key = str(key)
    #except ValueError:
    #    messagebox.showerror("Invalid ID", "Please enter a valid numeric ID.")
    #    return


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


    connect = sqlite3.connect("project_data.db")
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM Passenger WHERE oid = " + key)
    data = cursor.fetchone()

    if data:
         usernamePass.insert(0, data[1])
         emailPass.insert(0, data[2])
         passwordPass.insert(0, data[3])
         contactPass.insert(0, data[4])
         idPass.insert(0, data[5])
         age.insert(0, data[6])
         gender.insert(0, data[7])
         passportNum.insert(0, data[8])
         frequentFly.insert(0, data[9])

    else:
        pass

    connect.commit()
    connect.close()

    all_widgets += [usernamePass, emailPass, passwordPass, contactPass, idPass, age, gender, passportNum, frequentFly, label1, label2, label3, label4, label5, label6, label7, label8, label9]
    

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

    confirm = Button(frameR, text="Ok", command=lambda: updatepass2(str(entryId.get())))
    confirm.grid(row=0, column=2, padx=5)

    all_widgets += [frameR, labelId, entryId, confirm]


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
    cursor.execute("SELECT *, oid FROM Passenger")
    rows = cursor.fetchall()

    Layout = Label(frameR, text = "1Username:  2Email:  3Password:  4Contact_Number:  5ID:  6Age:  7Gender:  8Passport:  9:FrequentFly ")
    Layout.grid(row = 0, column = 1)
    # Print each row
    for i, row in enumerate(rows):  
        Data = Label(frameR, text= str(row) + ",")
        Data.grid(row=i+1, column=1, sticky='w')

    all_widgets += [Data, Layout, frameR]
        

    


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

button2 = Button(frameL, text = "Flights Section",width = 50, command = None, bd = 1)
button2.grid(row = 2, column = 0, padx = 10, pady = 10)

button3 = Button(frameL, text = "Contact Support", width = 50, command = None, bd = 1)
button3.grid(row = 3, column = 0, padx = 10, pady = 10)

button4 = Button(frameL, text = "Payments Section", width = 50, command = None, bd = 1)
button4.grid(row = 4, column = 0, padx = 10, pady = 10)

button5 = Button(frameL, text = "LogOut", width = 50, command = logout, bd = 1)
button5.grid(row = 5, column = 0, padx = 10, pady = 10)

buttonbox = Button(frameL, text = "🙂", command = root.quit)
buttonbox.grid(row = 6, column = 1, sticky = SE)





root.mainloop()