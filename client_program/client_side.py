# Application for creating and maintaining reservations
# for test drives of various cars

from tkinter import *
from tkinter import messagebox
import re
import Pmw
import socket
import time
import threading
import pickle
from client_program.classes.User_class import User
from client_program.user_interface import UserInterface
from client_program.classes.registration_form_class import RegistrationForm
from client_program.admin_interface import AdminInterface


# Creating main Window

main_window = Tk()
main_window.title("CaReserv")
main_window.geometry("500x500+550+200")
main_window.resizable(False, False)

# Connecting with server

client_socket = socket.socket()



def openingAConnectionToServer(host, port):
    global client_socket
    client_socket = socket.socket()
    succesful = FALSE
    while not succesful:
        try:
            client_socket.connect((host, port))
            succesful = TRUE
            connectingToServerFrame.pack_forget()
            openLoginPanel()
        except:
            connectingToServerFrame_lblReconnectingCounter.config(fg="darkred")
            CounterString.set("Unable to reconnect to the server!")
            time.sleep(2)
            countToZero()


def countToZero():
    connectingToServerFrame_lblReconnectingCounter.config(fg="darkgreen")
    for number in range (5, -1, -1):
        CounterString.set("Automatically reconnecting in ... " + str(number))
        time.sleep(1)
        CounterString.set("Please wait...")


connectingToServerFrame = Frame(main_window, bg="gray", pady="150")
connectingToServerFrame.pack(expand=TRUE, fill="both")
connectingToServerFrame_lblStatus = Label(connectingToServerFrame, text="Trying to connect to the server\nplease wait", bg="gray", font="Arial 16", fg="white", width="40")
connectingToServerFrame_lblStatus.grid(row=0)
CounterString = StringVar()
connectingToServerFrame_lblReconnectingCounter = Label(connectingToServerFrame, textvariable=CounterString, bg="gray", fg="white", font="Arial 16 bold")
connectingToServerFrame_lblReconnectingCounter.grid(row=1)
connectingToServerFrame_btnCloseApp = Button(connectingToServerFrame, text="Close App", command=main_window.destroy)
connectingToServerFrame_btnCloseApp.grid(row=2)
connectionThread = threading.Thread(target=lambda: openingAConnectionToServer(socket.gethostname(), 2020))
connectionThread.daemon = TRUE



# Login Panel

def openLoginPanel():
    LoginFrame.pack(expand=TRUE, fill="both")
    LoginFrame_entryUsername.config(textvariable=StringVar())
    LoginFrame_entryPassword.config(textvariable=StringVar())
    LoginFrame_entryUsername.focus_set()

def submitCredentials(client_socket):
    try:
        client_socket.send(
            ("LoginCredentials:" + LoginFrame_entryUsername.get() + ":" + LoginFrame_entryPassword.get()).encode())
        currentUser = User.tupleConstructor(pickle.loads(client_socket.recv(1024)))
        if currentUser.admin == "Yes":
            LoginFrame.pack_forget()
            adminInterface = AdminInterface(main_window, LoginFrame, client_socket, currentUser)
        elif currentUser.admin == "No":
            LoginFrame.pack_forget()
            userInterface = UserInterface(main_window, LoginFrame, client_socket, currentUser)
        else:
            messagebox.showerror("Wrong credentials!", "There is no user found with this username or password! "
                                                       "Please try different ones.\nIf you don't have an account already, please create a new one.")
        LoginFrame_entryUsername.config(textvariable=StringVar())
        LoginFrame_entryPassword.config(textvariable=StringVar())
        LoginFrame_entryUsername.focus_set()
    except ConnectionError:
        messagebox.showerror("Failed!", "Server isn't available right now, please try again later!")
        sys.exit()



def exitApp():
    if messagebox.askyesno("Leaving?", "Are you sure you want to exit the application?"):
        client_socket.close()
        sys.exit()


usernames = []
LoginFrame = Frame(main_window, bg="lightgray")

LoginFrame_lblTitle = Label(LoginFrame, text="Log into your account", font=('Arial', 20), bg="lightgray")
LoginFrame_lblTitle.pack()

LoginFrame_lblRegistrationPanelHyperlink = Label(LoginFrame, text="or create new account?", font=('Arial', 10), bg="lightgray", fg="blue", cursor="hand2")
LoginFrame_lblRegistrationPanelHyperlink.bind("<Button-1>", lambda x: openRegistrationPanel("openingRegistrationPanel"))
LoginFrame_lblRegistrationPanelHyperlink.pack()

LoginFrame_centerFrame = Frame(LoginFrame, pady=100, bg="lightgray")
LoginFrame_lblUsername = Label(LoginFrame_centerFrame, text="Username:", font=('Arial', 14), bg="lightgray")
LoginFrame_lblUsername.grid(row=0, column=0)
LoginFrame_entryUsername = Entry(LoginFrame_centerFrame)
LoginFrame_entryUsername.grid(row=0, column=1)
LoginFrame_entryUsername.focus_set()
LoginFrame_lblPassword = Label(LoginFrame_centerFrame, text="Password:", font=('Arial', 14), bg="lightgray")
LoginFrame_lblPassword.grid(row=1, column=0, pady=10)
LoginFrame_entryPassword = Entry(LoginFrame_centerFrame, show="*")
LoginFrame_entryPassword.grid(row=1, column=1)
LoginFrame_btnSubmitLoginInfo = Button(LoginFrame_centerFrame, text="Log in", font=('Arial', 14), bg="lightblue", command=lambda : submitCredentials(client_socket))
LoginFrame_btnSubmitLoginInfo.grid(columnspan=2, pady=30)

LoginFrame_centerFrame.pack()

LoginFrame_btnExitApp = Button(LoginFrame, bg="black", fg="white", text="Exit application", width=20, height=3,
                               font=("New Roman", 14, "bold"), cursor="hand2", command=exitApp)
LoginFrame_btnExitApp.pack()



# Registration Panel

def openRegistrationPanel(event):
    LoginFrame.pack_forget()
    RegistrationFrame.pack(expand=TRUE, fill="both")
    clearingEntries()
    try:
        client_socket.send("Users:".encode())
        users = pickle.loads(client_socket.recv(1024))
        usernames.clear()
        for user in users:
            usernames.append(user[6])
    except ConnectionError:
        messagebox.showerror("Failed!", "Server isn't available right now, please try again later!")
        sys.exit()

def entryValidation(entry):
    entry.widget.configure(bg="lightgreen")
    if entry.widget == RegistrationFrame_entryFirstName:
        if not re.match(r'^([A-Z][a-z]*(\s+[A-Z][a-z]*){,2})$', entry.widget.get()):
            entry.widget.configure(bg="red")

    if entry.widget == RegistrationFrame_entryLastName:
        if not re.match(r'^(()*[A-Z][a-z]*)$', entry.widget.get()):
            entry.widget.configure(bg="red")

    if entry.widget == RegistrationFrame_entryUsername:
        if RegistrationFrame_entryUsername.get() in usernames:
            entry.widget.configure(bg="red")

    if entry.widget == RegistrationFrame_entryPhoneNumber:
        if not re.match(r'^(\+?\d*)$', entry.widget.get()):
            entry.widget.configure(bg="red")

    if entry.widget == RegistrationFrame_entryEmail:
        if not re.match(r'^[\w+\.]+@[a-zA-Z0-9]+(\-)?[a-zA-Z0-9]+(\.)?[a-zA-Z0-9]{2,6}?\.[a-zA-Z]{2,6}$', entry.widget.get()):
            entry.widget.configure(bg="red")

    if entry.widget == RegistrationFrame_entryPassword:
        if not re.match(r'^((?=\S*?[A-Z])(?=\S*?[a-z])(?=\S*?[0-9]).{6,})\S$', entry.widget.get()):
            entry.widget.configure(bg="red")

    if entry.widget == RegistrationFrame_entryConfirmPassword:
        if not entry.widget.get() == RegistrationFrame_entryPassword.get():
            entry.widget.configure(bg="red")

    if entry.widget.get() == "":
        entry.widget.configure(bg="white")

def returnToLoginPanel():
    if len(list(filter(lambda x: len(x.get()) > 0, RegistrationFrame_listOfEntries))) > 0:
        if not messagebox.askyesno("Discard changes?",
                               "Are you sure you want to return to Login Panel? All changes you made here will be deleted."):
            return
    RegistrationFrame.pack_forget()
    openLoginPanel()

def submitRegistrationInfo():
    try:
        client_socket.send("New user:".encode())
        client_socket.send(pickle.dumps(
            User(0, RegistrationFrame_entryFirstName.get(), RegistrationFrame_entryLastName.get(),
                 RegistrationFrame_entryUsername.get(), RegistrationFrame_entryEmail.get()
                 , RegistrationFrame_entryPhoneNumber.get(),
                 RegistrationFrame_entryPassword.get(), "No")))
        if not client_socket.recv(1024).decode() == "Error":
            messagebox.showinfo("Successful!", "You have just registered your account, we hope you will enjoy with our services.")
        else:
            messagebox.showerror("Failed!", "Unfortunately, your registration request isn't completed, please try again later.")
    except ConnectionError:
        messagebox.showerror("Failed!", "Server isn't available right now, please try again later!")
        sys.exit()

def resetRegistration():
    if messagebox.askyesno("Clear all fields?", "Are you sure you want to discard all changes and clear fields from data you entered?"):
        clearingEntries()


def clearingEntries():
    for entry in RegistrationFrame_listOfEntries:
        entry.config(textvariable=StringVar(), bg="white")
    RegistrationFrame_entryFirstName.focus_set()


RegistrationFrame = Frame(main_window, bg="lightgray")

RegistrationFrame_lblTitle = Label(RegistrationFrame, text="Register your new account", font=('Arial', 20), bg="lightgray")
RegistrationFrame_lblTitle.pack()

 # Center Frame of Registration Frame
RegistrationFrame_centerFrame = Frame(RegistrationFrame, pady=50, bg="lightgray")



RegistrationFrame_lblFirstName = Label(RegistrationFrame_centerFrame, text="First name:", font=('Arial',14), bg="lightgray", anchor="e")
RegistrationFrame_lblFirstName.grid(row=0, column=0, sticky="e", pady=6)
RegistrationFrame_entryFirstName = Entry(RegistrationFrame_centerFrame)
RegistrationFrame_entryFirstName.focus_set()
RegistrationFrame_entryFirstName.grid(row=0, column=1)
RegistrationFrame_entryFirstName.bind("<FocusOut>", entryValidation)
widgetTooltip = Pmw.Balloon(RegistrationFrame)
widgetTooltip.bind(RegistrationFrame_entryFirstName, "NOTE: Only first letter of the word can be capital,\nname can be maximum 3 words long, "
                                     "\nand each of them to be at least 2 letters long. \nNo digits are allowed.\nWrong: Mary jane\nCorrect: Mary Jane")

RegistrationFrame_lblLastName = Label(RegistrationFrame_centerFrame, text="Last name:", font=('Arial',14), bg="lightgray")
RegistrationFrame_lblLastName.grid(row=1,column=0, sticky="e", pady=6)
RegistrationFrame_entryLastName = Entry(RegistrationFrame_centerFrame)
RegistrationFrame_entryLastName.grid(row=1,column=1)
RegistrationFrame_entryLastName.bind("<FocusOut>", entryValidation)
widgetTooltip.bind(RegistrationFrame_entryLastName, "NOTE: Only first letter of the word can be capital,\nname can be maximum 3 words long, "
                                         "\nand each of them to be at least 2 letters long. \nNo digits are allowed.\nWrong: von der Malsburg\nCorrect: Von Der Malsburg")

RegistrationFrame_lblUsername = Label(RegistrationFrame_centerFrame, text="Username:", font=('Arial',14), bg="lightgray")
RegistrationFrame_lblUsername.grid(row=2, column=0, sticky="e", pady=6)
RegistrationFrame_entryUsername = Entry(RegistrationFrame_centerFrame)
RegistrationFrame_entryUsername.grid(row=2,column=1)
RegistrationFrame_entryUsername.bind("<FocusOut>", entryValidation)

RegistrationFrame_lblEmail = Label(RegistrationFrame_centerFrame, text="Email:", font=('Arial',14), bg="lightgray")
RegistrationFrame_lblEmail.grid(row=3,column=0, sticky="e", pady=6)
RegistrationFrame_entryEmail = Entry(RegistrationFrame_centerFrame)
RegistrationFrame_entryEmail.grid(row=3,column=1)
RegistrationFrame_entryEmail.bind("<FocusOut>", entryValidation)
widgetTooltip.bind(RegistrationFrame_entryEmail, "NOTE: Standard email format - \"local-part@domain\"\nExample: john.smith00@gmail.com")

RegistrationFrame_lblPhoneNumber = Label(RegistrationFrame_centerFrame, text="Phone number:", font=('Arial',14), bg="lightgray")
RegistrationFrame_lblPhoneNumber.grid(row=4,column=0, sticky="e", pady=6)
RegistrationFrame_entryPhoneNumber = Entry(RegistrationFrame_centerFrame)
RegistrationFrame_entryPhoneNumber.grid(row=4,column=1)
RegistrationFrame_entryPhoneNumber.bind("<FocusOut>", entryValidation)
widgetTooltip.bind(RegistrationFrame_entryPhoneNumber, "NOTE: Starts with the country code - \"+381\" for Serbia etc, only digits allowed. \nNo white spaces between digits.\nWrong: +381 65 456 789\nCorrect: +38165456789")

RegistrationFrame_lblPassword = Label(RegistrationFrame_centerFrame, text="Password:", font=('Arial',14), bg="lightgray")
RegistrationFrame_lblPassword.grid(row=5,column=0, sticky="e", pady=6)
RegistrationFrame_entryPassword = Entry(RegistrationFrame_centerFrame, show="*")
RegistrationFrame_entryPassword.grid(row=5,column=1)
RegistrationFrame_entryPassword.bind("<FocusOut>", entryValidation)
widgetTooltip.bind(RegistrationFrame_entryPassword, "NOTE: Password minimum requirements:\n\t- 6 characters\n\t- 1 uppercase letter,\n\t- 1 lowercase letter,"
                                                "\n\t- 1 digit\nNo space allowed.")

RegistrationFrame_lblConfirmPassword = Label(RegistrationFrame_centerFrame, text="Confirm password:", font=('Arial',14), bg="lightgray", wraplength=90)
RegistrationFrame_lblConfirmPassword.grid(row=6, column=0, sticky="e", pady=6)
RegistrationFrame_entryConfirmPassword = Entry(RegistrationFrame_centerFrame, show="*")
RegistrationFrame_entryConfirmPassword.grid(row=6, column=1)
RegistrationFrame_entryConfirmPassword.bind("<FocusOut>", entryValidation)

RegistrationFrame_centerFrame.pack()

RegistrationFrame_listOfEntries =[RegistrationFrame_entryFirstName, RegistrationFrame_entryLastName, RegistrationFrame_entryUsername, RegistrationFrame_entryPhoneNumber, RegistrationFrame_entryEmail
                                  , RegistrationFrame_entryEmail, RegistrationFrame_entryPassword, RegistrationFrame_entryConfirmPassword]

  # Bottom Frame of Registration Frame
RegistrationFrame_bottomFrame = Frame(RegistrationFrame, bg="lightgray")

RegistrationFrame_btnReturn = Button(RegistrationFrame_bottomFrame,  text="< - Back", command=returnToLoginPanel, font=('Arial', 14), bg="lightyellow")
RegistrationFrame_btnReturn.grid(row=0, column=0, padx=40, sticky="e")
RegistrationFrame_btnSubmitRegistration = Button(RegistrationFrame_bottomFrame, text="Register", command=submitRegistrationInfo, font=('Arial', 14), bg="lightblue")
RegistrationFrame_btnSubmitRegistration.grid(row=0, column=1, padx=40, sticky="e")
RegistrationFrame_btnResetRegistration = Button(RegistrationFrame_bottomFrame, text="Reset", command=resetRegistration, font=('Arial', 14), bg="red")
RegistrationFrame_btnResetRegistration.grid(row=0, column=2, padx=40, sticky="e")

RegistrationFrame_bottomFrame.pack()



# Mainloop
connectionThread.start()
main_window.mainloop()
