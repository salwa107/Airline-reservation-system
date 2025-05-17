from tkinter import *
root = Tk()
root.title("Airplan Reservation System Project")

#the sign up method to save the new data to database
def SignUp():
    global signwindow
    signwindow = Tk()
    signwindow.title("Sign Up Window")
    signwindow.geometry("400x400")

    global entry1
    global entry2
    global entry3
    global entry4
    global entry5



    confirmbut = Button(signwindow, text = "Confirm", command = newaccount).grid()

#method of new account to db
def newaccount():
    #the database update


    #crash the window
    signwindow.destroy()


#the checkmethod after clicking the cont button
### need lots if fixes ###
def checkmethod():
    Name = entryName.get()
    Password = entryPassword.get()

    #if name or password wasn't filled (Empty Strings)

    #if the name and password are existed (Sign in)

    #if the username is existed (To Sign Up)

    #if the password is wrong (Return False)


#defining the Label frames
framebg = LabelFrame(root, padx = 50, pady = 50, bg = "Sky Blue")
frame1 = LabelFrame(framebg, text = "Welcome" , padx = 100, pady = 100, bd = 1, bg = "Light Gray")
framebg.pack(padx = 25, pady = 25)
frame1.pack(padx = 100 , pady = 100)

#defining the Widgets
entryName = Entry(frame1, bd = 1, width = 50)
namelabel = Label(frame1, text = "Name", bg= "Light Gray")
entryPassword = Entry(frame1, bd = 1 , width = 50)
passwordlabel = Label(frame1, text = "Password", bg= "Light Gray")

buttonEnd = Button(frame1, text = "Quit" , padx = 1 , pady = 1,command = root.quit)
buttonCont = Button(frame1, text = "Continue" , padx = 1, pady = 1, command = checkmethod)
buttonUp = Button(frame1, text = "Sign Up", padx = 1, pady = 1, command = SignUp)




#Shoving Widgets
entryName.grid(column = 1 , row = 1, columnspan= 2, pady = (0, 10))
namelabel.grid(column = 0, row = 1, pady = (0, 10))
entryPassword.grid(column = 1 , row = 2, columnspan= 2, pady = (0, 10))
passwordlabel.grid(column = 0, row = 2, pady = (0, 10))


buttonEnd.grid(column = 0, row = 3, columnspan = 2)
buttonCont.grid(column = 0, row = 3, columnspan = 3)
buttonUp.grid(column = 2, row = 3, columnspan = 1)

root.mainloop()