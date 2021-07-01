
from tkinter import *
import Pmw
import pickle

class RegistrationForm(Frame):
    def __init__(self, parent, client_socket, currentUser, *args, **kwargs):
        Frame.__init__(self, master=parent, *args, *kwargs)
        self.parent = parent
        self.client_socket = client_socket
        self.currentUser = currentUser

        self.lblFirstName = Label(self, text="First name:", font=('Arial', 14),
                                               bg=parent.cget("bg"), anchor="e")
        self.lblFirstName.place(rely=0.03, relheight=0.1, relx=0.1, relwidth=0.3)
        self.entryFirstName = Entry(self)
        self.entryFirstName.focus_set()
        self.entryFirstName.place(rely=0.03, relheight=0.1, relx=0.43, relwidth=0.47)
        self.entryFirstName.bind("<FocusOut>", self.entryValidation)
        self.widgetTooltip = Pmw.Balloon(self.parent)
        self.widgetTooltip.bind(self.entryFirstName,
                           "NOTE: Only first letter of the word can be capital,\nname can be maximum 3 words long, "
                           "\nand each of them to be at least 2 letters long. \nNo digits are allowed.\nWrong: Mary jane\nCorrect: Mary Jane")

        self.lblLastName = Label(self, text="Last name:", font=('Arial', 14),
                                              bg=parent.cget("bg"), anchor="e")
        self.lblLastName.place(rely=0.17, relheight=0.1, relx=0.1, relwidth=0.3)
        self.entryLastName = Entry(self)
        self.entryLastName.place(rely=0.17, relheight=0.1, relx=0.43, relwidth=0.47)
        self.entryLastName.bind("<FocusOut>", self.entryValidation)
        self.widgetTooltip.bind(self.entryLastName,
                           "NOTE: Only first letter of the word can be capital,\nname can be maximum 3 words long, "
                           "\nand each of them to be at least 2 letters long. \nNo digits are allowed.\nWrong: von der Malsburg\nCorrect: Von Der Malsburg")

        self.lblUsername = Label(self, text="Username:", font=('Arial', 14),
                                              bg=parent.cget("bg"), anchor="e")
        self.lblUsername.place(rely=0.31, relheight=0.1, relx=0.1, relwidth=0.3)
        self.entryUsername = Entry(self)
        self.entryUsername.place(rely=0.31, relheight=0.1, relx=0.43, relwidth=0.47)
        self.entryUsername.bind("<FocusOut>", self.entryValidation)

        self.lblEmail = Label(self, text="Email:", font=('Arial', 14),
                                           bg=parent.cget("bg"), anchor="e")
        self.lblEmail.place(rely=0.45, relheight=0.1, relx=0.1, relwidth=0.3)
        self.entryEmail = Entry(self)
        self.entryEmail.place(rely=0.45, relheight=0.1, relx=0.43, relwidth=0.47)
        self.entryEmail.bind("<FocusOut>", self.entryValidation)
        self.widgetTooltip.bind(self.entryEmail,
                           "NOTE: Standard email format - \"local-part@domain\"\nExample: john.smith00@gmail.com")

        self.lblPhoneNumber = Label(self, text="Phone number:",
                                    font=('Arial', 14), bg=parent.cget("bg"), anchor="e")
        self.lblPhoneNumber.place(rely=0.59, relheight=0.1, relx=0.1, relwidth=0.3)
        self.entryPhoneNumber = Entry(self)
        self.entryPhoneNumber.place(rely=0.59, relheight=0.1, relx=0.43, relwidth=0.47)
        self.entryPhoneNumber.bind("<FocusOut>", self.entryValidation)
        self.widgetTooltip.bind(self.entryPhoneNumber,
                                "NOTE: Starts with the country code - \"+381\" for Serbia etc, only digits allowed. \nNo white spaces between digits.\nWrong: +381 65 456 789\nCorrect: +38165456789")

        self.lblPassword = Label(self, text="Password:", font=('Arial', 14),
                                              bg=parent.cget("bg"), anchor="e")
        self.lblPassword.place(rely=0.73, relheight=0.1, relx=0.1, relwidth=0.3)
        self.entryPassword = Entry(self, show="*")
        self.entryPassword.place(rely=0.73, relheight=0.1, relx=0.43, relwidth=0.47)
        self.entryPassword.bind("<FocusOut>", self.entryValidation)
        self.widgetTooltip.bind(self.entryPassword,
                           "NOTE: Password minimum requirements:\n\t- 6 characters\n\t- 1 uppercase letter,\n\t- 1 lowercase letter,"
                           "\n\t- 1 digit\nNo space allowed.")

        self.lblConfirmPassword = Label(self, text="Confirm password:",
                                                     font=('Arial', 14), bg=parent.cget("bg"), wraplength=90, anchor="e")
        self.lblConfirmPassword.place(rely=0.85, relheight=0.14, relx=0.1, relwidth=0.3)
        self.entryConfirmPassword = Entry(self, show="*")
        self.entryConfirmPassword.place(rely=0.85, relheight=0.1, relx=0.43, relwidth=0.47)
        self.entryConfirmPassword.bind("<FocusOut>", self.entryValidation)

        self.listOfEntries = [self.entryFirstName, self.entryLastName,self.entryUsername, self.entryEmail,
                              self.entryPhoneNumber, self.entryPassword, self.entryConfirmPassword]

    def entryValidation(self, entry):
        entry.widget.configure(bg="lightgreen")
        usernames = list()
        if entry.widget == self.entryFirstName:
            if not re.match(r'^([A-Z][a-z]*(\s+[A-Z][a-z]*){,2})$', entry.widget.get()):
                entry.widget.configure(bg="red")

        if entry.widget == self.entryLastName:
            if not re.match(r'^(()*[A-Z][a-z]*)$', entry.widget.get()):
                entry.widget.configure(bg="red")

        if entry.widget == self.entryUsername:
            self.client_socket.send("Usernames:".encode())
            databaseResult = pickle.loads(self.client_socket.recv(1024))
            for username in databaseResult:
                usernames.append(username)
            if self.entryUsername.get() in usernames:
                entry.widget.configure(bg="red")

        if entry.widget == self.entryPhoneNumber:
            if not re.match(r'^(\+?\d*)$', entry.widget.get()):
                entry.widget.configure(bg="red")

        if entry.widget == self.entryEmail:
            if not re.match(r'^[\w+\.]+@[a-zA-Z0-9]+(\-)?[a-zA-Z0-9]+(\.)?[a-zA-Z0-9]{2,6}?\.[a-zA-Z]{2,6}$',
                            entry.widget.get()):
                entry.widget.configure(bg="red")

        if entry.widget == self.entryPassword:
            if not re.match(r'^((?=\S*?[A-Z])(?=\S*?[a-z])(?=\S*?[0-9]).{6,})\S$', entry.widget.get()):
                entry.widget.configure(bg="red")

        if entry.widget == self.entryConfirmPassword:
            if not entry.widget.get() == self.entryPassword.get():
                entry.widget.configure(bg="red")

        if entry.widget.get() == "":
            entry.widget.configure(bg="white")

    def setEntries(self, listOfEntries):
        for entry in listOfEntries:
            entry.config(bg="lightgreen")
        self.entryConfirmPassword.config(bg="white")

        self.entryFirstName.config(textvariable=StringVar(value=self.currentUser.firstName))
        self.entryLastName.config(textvariable=StringVar(value=self.currentUser.lastName))
        self.entryUsername.config(textvariable=StringVar(value=self.currentUser.username))
        self.entryPhoneNumber.config(textvariable=StringVar(value=self.currentUser.phone))
        self.entryEmail.config(textvariable=StringVar(value=self.currentUser.email))
        self.entryPassword.config(textvariable=StringVar(value=self.currentUser.password))
        tupleUser = self.currentUser.toTuple()
        for i in range(5):
            listOfEntries[i].config(textvariable=StringVar(value=tupleUser[i+1]))
