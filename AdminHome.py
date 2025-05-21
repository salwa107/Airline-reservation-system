from tkinter import *
import subprocess
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

    upButPass = Button(Passframe, text = "Update Data", width = 15, command = None, bd = 1)
    upButPass.grid(row = 1, column = 0, padx = (10, 50), pady = (10, 10), sticky = W)

    delButPass = Button(Passframe, text = "Delete Data", width = 15, command = None, bd = 1)
    delButPass.grid(row = 2, column = 0, padx = (10, 50), pady = (10, 10), sticky = W)

    exitPass = Button(Passframe, text = " Exit", width = 15, command = PassWin.destroy, bd = 1)
    exitPass.grid(row = 3, column = 0, padx = (10, 50), pady = (10, 10), sticky = W)

###########################################

def updatepass():

    global all_widgets
    global s

    for widget in all_widgets:
        widget.destroy()
    all_widgets = []

    frameR = LabelFrame(PassWin, text = "Update")
    frameR.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = E)

    


    all_widgets += [frameR]

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
    cursor.execute("SELECT *, oid FROM Administrator")
    rows = cursor.fetchall()

    Layout = Label(frameR, text = "1Username:  2Email:  3Password:  4Contack_Number:  5ID:  6Role: ")
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