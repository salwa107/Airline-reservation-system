from tkinter import *
from tkinter import messagebox
import subprocess
import sqlite3

root = Tk()
root.title("Airplan Reservation System Project")
#root.iconbitmap("D:\University\Programmes\Foundamental\PROJECTS\Mini Project1\Airline-reservation-system\Airline-reservation-system\Photos\airline_icon.ico")

#the sign up method to save the new data to database
widgetlist = []

def SignUp2(valu):
    
    global usernamePass, emailPass, passwordPass, contactPass, idPass, age, gender, passportNum, frequentFly
    global label1, label2, label3, label4, label5, label6, label7, label8, label9
    global usernameAdmin, emailAdmin, passwordAdmin, contactAdmin, idAdmin, role
    global label11, label22, label33, label44, label55, label66
    global widgetlist, confirmfinal

    # Destroy and clear the old widgets
    for widget in widgetlist:
        widget.destroy()
    widgetlist = []

    if valu == 1:
        label1 = Label(signwindow, text="UserName")
        label1.grid(row=3, column=0, pady=(5, 5))
        usernamePass = Entry(signwindow, width=50)
        usernamePass.grid(row=3, column=1, pady=(5, 5))

        label2 = Label(signwindow, text="Email")
        label2.grid(row=4, column=0, pady=(5, 5))
        emailPass = Entry(signwindow, width=50)
        emailPass.grid(row=4, column=1, pady=(5, 5))

        label3 = Label(signwindow, text="Password")
        label3.grid(row=5, column=0, pady=(5, 5))
        passwordPass = Entry(signwindow, width=50)
        passwordPass.grid(row=5, column=1, pady=(5, 5))

        label4 = Label(signwindow, text="ContactNumber")
        label4.grid(row=6, column=0, pady=(5, 5))
        contactPass = Entry(signwindow, width=50)
        contactPass.grid(row=6, column=1, pady=(5, 5))

        label5 = Label(signwindow, text="National ID")
        label5.grid(row=7, column=0, pady=(5, 5))
        idPass = Entry(signwindow, width=50)
        idPass.grid(row=7, column=1, pady=(5, 5))

        label6 = Label(signwindow, text="Age")
        label6.grid(row=8, column=0, pady=(5, 5))
        age = Entry(signwindow, width=50)
        age.grid(row=8, column=1, pady=(5, 5))

        label7 = Label(signwindow, text="Gender")
        label7.grid(row=9, column=0, pady=(5, 5))
        gender = Entry(signwindow, width=50)
        gender.grid(row=9, column=1, pady=(5, 5))

        label8 = Label(signwindow, text="PassportNumber")
        label8.grid(row=10, column=0, pady=(5, 5))
        passportNum = Entry(signwindow, width=50)
        passportNum.grid(row=10, column=1, pady=(5, 5))

        label9 = Label(signwindow, text="FrequentFly")
        label9.grid(row=11, column=0, pady=(5, 5))
        frequentFly = Entry(signwindow, width=50)
        frequentFly.grid(row=11, column=1, pady=(5, 5))

        confirmfinal = Button(signwindow, text = "Confirm", command = lambda: newaccount(user.get()))
        confirmfinal.grid(row = 12, column = 1, columnspan = 1)

        widgetlist += [label1, usernamePass, label2, emailPass, label3, passwordPass,
                       label4, contactPass, label5, idPass, label6, age,
                       label7, gender, label8, passportNum, label9, frequentFly, confirmfinal]
        
    #################################################


    elif valu == 2:
        label11 = Label(signwindow, text="UserName")
        label11.grid(row=3, column=0, pady=(5, 5))
        usernameAdmin = Entry(signwindow, width=50)
        usernameAdmin.grid(row=3, column=1, pady=(5, 5))

        label22 = Label(signwindow, text="Email")
        label22.grid(row=4, column=0, pady=(5, 5))
        emailAdmin = Entry(signwindow, width=50)
        emailAdmin.grid(row=4, column=1, pady=(5, 5))

        label33 = Label(signwindow, text="Password")
        label33.grid(row=5, column=0, pady=(5, 5))
        passwordAdmin = Entry(signwindow, width=50)
        passwordAdmin.grid(row=5, column=1, pady=(5, 5))

        label44 = Label(signwindow, text="ContactNumber")
        label44.grid(row=6, column=0, pady=(5, 5))
        contactAdmin = Entry(signwindow, width=50)
        contactAdmin.grid(row=6, column=1, pady=(5, 5))

        label55 = Label(signwindow, text="National ID")
        label55.grid(row=7, column=0, pady=(5, 5))
        idAdmin = Entry(signwindow, width=50)
        idAdmin.grid(row=7, column=1, pady=(5, 5))

        label66 = Label(signwindow, text="Role")
        label66.grid(row=8, column=0, pady=(5, 5))
        role = Entry(signwindow, width=50)
        role.grid(row=8, column=1, pady=(5, 5))

        confirmfinal = Button(signwindow, text = "Confirm", command = lambda: newaccount(user.get()))
        confirmfinal.grid(row = 9, column = 1, columnspan = 1)

        widgetlist += [label11, usernameAdmin, label22, emailAdmin, label33, passwordAdmin,
                       label44, contactAdmin, label55, idAdmin, label66, role, confirmfinal]



#################################################
#################################################

    


#choose kind of user for sign up or Login
def SignUp1():
    global signwindow
    signwindow = Toplevel()
    signwindow.title("Sign Up Window")
    #signwindow.iconbitmap("Airline-reservation-system\Photos\airline_icon.ico")
    signwindow.geometry("800x400")

    #Radiobuttons variable definition
    global user
    user = IntVar()
    user.set(1)
    
    #Radiobuttons
    Radiobutton(signwindow, text = "Passenger", variable = user, value = 1).grid(row = 0, column = 0, padx = (10,0))
    Radiobutton(signwindow, text = "Adminstrator", variable = user, value = 2).grid(row = 1, column = 0, padx = (10,0))
    

    confirm1 = Button(signwindow, text = "Next", command = lambda: SignUp2(user.get())).grid(row = 2, column = 1, padx = (50,0))
    cancle = Button(signwindow, text = "Cancel", command = signwindow.destroy).grid(row = 2, column = 0)


#################################################
#################################################


#method of new account to db
def newaccount(value):
    
    #the database update
    #if for Passenger
    if value == 1:
        


        connect = sqlite3.connect("project_data.db")
        cursor = connect.cursor()

        cursor.execute(
            "INSERT INTO Passenger VALUES(:usernamePass, :emailPass, :passwordPass, :contactPass, :idPass, :age, :gender, :passportNum, :frequentFly)",
            {
            "usernamePass": usernamePass.get(),
            "emailPass": emailPass.get(),
            "passwordPass": passwordPass.get(),
            "contactPass": contactPass.get(),
            "idPass": idPass.get(),
            "age": age.get(),
            "gender": gender.get(),
            "passportNum": passportNum.get(),
            "frequentFly": frequentFly.get()
            }
            )
        
        connect.commit()
        connect.close()

        #crash the window
        signwindow.destroy()


        #Label(signwindow, text = "this is 1").grid()

    #####################################################

    #else if for Administrator
    elif value == 2:


        connect = sqlite3.connect("project_data.db")
        cursor = connect.cursor()
        cursor.execute(
            "INSERT INTO Administrator VALUES(:usernameAdmin, :emailAdmin, :passwordAdmin, :contactAdmin, :idAdmin, :role)",
            {
            "usernameAdmin": usernameAdmin.get(),
            "emailAdmin": emailAdmin.get(),
            "passwordAdmin": passwordAdmin.get(),
            "contactAdmin": contactAdmin.get(),
            "idAdmin": idAdmin.get(),
            "role": role.get()
            }
        )

        
        connect.commit()
        connect.close()

        #crash the window
        signwindow.destroy()
    
    #################################################
    #################################################



#the checkmethod after clicking the cont button
### need lots if fixes ###

def checkmethod(value):

    #if name or password wasn't filled (Empty Strings)
    #if the name and password are existed (Sign in)
    #if the username is existed (To Sign Up)
    #if the password is wrong (Return False)

    if value == 1:
        
        connect = sqlite3.connect("project_data.db")
        cursor = connect.cursor()
        
        cursor.execute("SELECT 1 FROM Passenger WHERE email = ? AND password = ?", (entryName.get(), entryPassword.get()))
        result = cursor.fetchone()


        if result:
            
            subprocess.Popen(["python", "Airline-reservation-system\passenger.py"])
            root.quit()

        else:
            R1 = messagebox.showerror("Wrong Data", "mail or Password isn't True, Try again!!")

        connect.commit()
        connect.close()

    elif value == 2:
        
        connect = sqlite3.connect("project_data.db")
        cursor = connect.cursor()

        #SELECT 1 is used because we only care whether a match exists, not the actual data
        cursor.execute("SELECT 1 FROM Administrator WHERE email = ? AND password = ?", (entryName.get(), entryPassword.get()))
        result = cursor.fetchone()


        if result:
            
            subprocess.Popen(["python", "Airline-reservation-system\AdminHome.py"])
            root.quit()

        else:
            R = messagebox.showerror("Wrong Data", "mail or Password isn't True, Try again!!")
            
        
        ##
        connect.commit()
        connect.close()
        

        

    
#################################################
#################################################


#defining the Label frames
framebg = LabelFrame(root, padx = 50, pady = 50, bg = "Sky Blue")
frame1 = LabelFrame(framebg, text = "Welcome" , padx = 100, pady = 100, bd = 1, bg = "Light Gray")
framebg.pack(padx = 25, pady = 25)
frame1.pack(padx = 100 , pady = 100)

#defining the Widgets
global entryName
global entryPassword

entryName = Entry(frame1, bd = 1, width = 50)
namelabel = Label(frame1, text = "Email", bg= "Light Gray")
entryPassword = Entry(frame1, bd = 1 , width = 50)
passwordlabel = Label(frame1, text = "Password", bg= "Light Gray")

buttonEnd = Button(frame1, text = "Quit" , padx = 1 , pady = 1,command = root.quit)
buttonCont = Button(frame1, text = "Continue" , padx = 1, pady = 1, command = lambda: checkmethod(user1.get()))
buttonUp = Button(frame1, text = "Sign Up", padx = 1, pady = 1, command = SignUp1)


#Shoving Widgets
entryName.grid(column = 1 , row = 1, columnspan= 2, pady = (0, 10))
namelabel.grid(column = 0, row = 1, pady = (0, 10))
entryPassword.grid(column = 1 , row = 2, columnspan= 2, pady = (0, 10))
passwordlabel.grid(column = 0, row = 2, pady = (0, 10))


buttonEnd.grid(column = 0, row = 3, columnspan = 2)
buttonCont.grid(column = 0, row = 3, columnspan = 3)
buttonUp.grid(column = 2, row = 3, columnspan = 1)

#Radiobuttons 2
global user1
user1 = IntVar()
user1.set(1)
    
Radiobutton(frame1, text = "Passenger", variable = user1, value = 1,  background = "Light Gray").grid(row = 4, column = 1, pady = (10,0), padx = (10,0))
Radiobutton(frame1, text = "Adminstrator", variable = user1, value = 2, background = "Light Gray").grid(row = 4, column = 2, pady = (10,0), padx = (10,0))

root.mainloop()