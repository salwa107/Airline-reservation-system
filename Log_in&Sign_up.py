from tkinter import *
root = Tk()
root.title("Airplan Reservation System Project")

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
framebg = LabelFrame(root, padx = 100, pady = 100, bg = "Sky Blue")
frame1 = LabelFrame(framebg, text = "Welcome" , padx = 200, pady = 200, bd = 1, bg = "Light Gray")
framebg.pack(padx = 25, pady = 25)
frame1.pack(padx = 100 , pady = 100)

#defining the Widgets
entryName = Entry(frame1, bd = 1, width = 50)
entryPassword = Entry(frame1, bd = 1 , width = 50)

buttonEnd = Button(frame1, text = "Quit" , padx = 1 , pady = 1,command = root.quit)
buttonCont = Button(frame1, text = "Continue" , padx = 1, pady = 1, command = checkmethod)
buttonUp = Button(frame1, text = "Sign Up", padx = 1, pady = 1, command = None)

Space1 = Label(frame1, text = "", bg = "Light Gray")
Space2 = Label(frame1, text = "", bg = "Light Gray")

#test to memory the name in variables
nnn = str()
sss = str()

entryName.insert(0, "Name: " + nnn)
entryPassword.insert(0, "Password: " + sss)

#Shoving Widgets
entryName.grid(column = 1 , row = 1, columnspan= 2)
Space1.grid(column = 1, row = 2)
entryPassword.grid(column = 1 , row = 3, columnspan= 2)
Space2.grid(column = 1, row = 4)


buttonEnd.grid(column = 0, row = 5, columnspan = 2)
buttonCont.grid(column = 1, row = 5, columnspan = 2)
buttonUp.grid(row = 5, column = 2, columnspan = 2)

root.mainloop()