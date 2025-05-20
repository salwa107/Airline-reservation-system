from tkinter import *
import subprocess
root = Tk()
root.title("Airplan Reservation System Project/AdminHome")
#root.geometry("800x600")
#root.grid_columnconfigure(0, weight=1)
#root.grid_columnconfigure(1, weight=2)
#root.grid_rowconfigure(0, weight=1)


#frameR = LabelFrame(root, text = "BLUH BLUH!!", padx = 300, pady = 300)
#frameR.grid(row = 0, column = 1, padx = 10, pady = 10, sticky= "nsew")

#HOW TO ADD TWO FRAMES BESIDE EACH OTHER IN ONE FRAME????
#HOW TO SEND THE INFORMATION FROM THE LOGIN TO THE ADMIN FILE AND TO PASSENGER FILE

def logout():
    root.quit()
    subprocess.Popen(["python", "Airline-reservation-system\Log_in&Sign_up.py"])

frameL = LabelFrame(root, text = "Home Sweet Home!!", padx = 100, pady = 300, bg = "#d2cfcf")
frameL.grid(row = 0, column = 0,padx = 10, pady = 10, sticky= "nsew")

##
button1 = Button(frameL, text = "Passenger Section", width = 50, command = None, bd = 1)
button1.grid(row = 1, column = 0, padx = 10, pady = 10)

button2 = Button(frameL, text = "Flights Section",width = 50, command = None, bd = 1)
button2.grid(row = 2, column = 0, padx = 10, pady = 10)

button3 = Button(frameL, text = "Contact Support", width = 50, command = None, bd = 1)
button3.grid(row = 3, column = 0, padx = 10, pady = 10)

button4 = Button(frameL, text = "Payments Section", width = 50, command = None, bd = 1)
button4.grid(row = 4, column = 0, padx = 10, pady = 10)

button5 = Button(frameL, text = "LogOut", width = 50, command = logout, bd = 1)
button5.grid(row = 5, column = 0, padx = 10, pady = 10)






root.mainloop()