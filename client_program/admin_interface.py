

# This is the panel where user goes after successful login as an Admin


from tkinter import *
from tkinter import messagebox
import pickle
from client_program.classes.scrollable_frame_class import ScrollableFrame_AdminInterface
from client_program.classes.edit_car_form_class import CarInfoForm_Frame

class AdminInterface:
    def __init__(self, parent, LoginFrame, client_socket, currentUser):
        self.parent = parent
        self.loginFrame = LoginFrame
        self.client_socket = client_socket
        self.currentUser = currentUser

        # Creating Navigation Bar
        self.AdminInterfaceMainFrame = Frame(parent)
        self.AdminInterfaceMainFrame.pack(expand=TRUE, fill="both")
        self.AdminInterfaceMainFrame_NavigationFrame = Frame(self.AdminInterfaceMainFrame, bg="purple")
        self.AdminInterfaceMainFrame_NavigationFrame.place(relwidth=1.0, relheight=0.12)

        # Users frame Link
        self.UsersNavigationLink = Button(self.AdminInterfaceMainFrame_NavigationFrame, bg="white", fg="black",
                                                         text="Users", font=("Arial", "11"), bd=1,
                                                         relief="groove")
        self.UsersNavigationLink.bind("<Button-1>",lambda x: self._navigationBarClickHandler("users"))
        self.UsersNavigationLink.place(relx=0.04, relwidth=0.2, relheight=1.0)

        # Cars frame link
        self.CarsNavigationLink = Button(self.AdminInterfaceMainFrame_NavigationFrame, bg="purple", fg="white",
                                                   text="Cars", font=("Arial", "11"), bd=1,
                                                   relief="groove")
        self.CarsNavigationLink.bind("<Button-1>", lambda x: self._navigationBarClickHandler("cars"))
        self.CarsNavigationLink.place(relx=0.24, relwidth=0.2, relheight=1.0)

        # Reservations frame link
        self.ReservationsNavigationLink = Button(self.AdminInterfaceMainFrame_NavigationFrame, bg="purple", fg="white",
                                                text="Reservations", font=("Arial", "11"), bd=1,
                                                relief="groove")
        self.ReservationsNavigationLink.bind("<Button-1>", lambda x: self._navigationBarClickHandler("reservations"))
        self.ReservationsNavigationLink.place(relx=0.44, relwidth=0.2, relheight=1.0)

        # username of connected admin
        self.usernameLabel = Label(self.AdminInterfaceMainFrame_NavigationFrame,
                                   textvariable=StringVar(value=currentUser.username), justify=CENTER, bg="purple", fg="white",
                                   font=("Arial", "14"))
        self.usernameLabel.place(relx=0.65, relwidth=0.34, relheight=0.4, rely=0.05)

        # Link for logging out of account
        self.LogOutNavigationLink = Button(self.AdminInterfaceMainFrame_NavigationFrame, bg="purple", text="Log Out", fg="white",
                                           font=("Arial", "11"), bd=1, relief="groove", command=lambda: self.logOut())
        self.LogOutNavigationLink.place(relx=0.72, relwidth=0.2, relheight=0.5, rely=0.5)

        # Creating references to Frame for each selection in navbar
        self.AdminInterfaceMainFrame_UsersFrame = Frame(self.AdminInterfaceMainFrame, bg="pink")
        self.AdminInterfaceMainFrame_UsersFrame.place(rely=0.12, relheight=0.88, relwidth=1.0)
        self._UsersEditing()
        self.AdminInterfaceMainFrame_CarsFrame = Frame(self.AdminInterfaceMainFrame, bg="pink")
        self.AdminInterfaceMainFrame_ReservationsFrame = Frame(self.AdminInterfaceMainFrame, bg="pink")

        # Lists of links and frames they are reference of
        self.listOfNavigationOptions = (self.UsersNavigationLink, self.CarsNavigationLink, self.ReservationsNavigationLink)
        self.listOfFrames = (self.AdminInterfaceMainFrame_UsersFrame, self.AdminInterfaceMainFrame_CarsFrame,
                             self.AdminInterfaceMainFrame_ReservationsFrame)


    # Function that handles switching through the navbar links
    def _navigationBarClickHandler(self, option_selected):
        list(map(lambda x: x.config(bg="purple", fg="white"), self.listOfNavigationOptions))
        list(map(lambda x: x.place_forget(), self.listOfFrames))
        if option_selected == "users":
            self.UsersNavigationLink.config(bg="white", fg="black")
            self._UsersEditing()
        elif option_selected == "cars":
            self.CarsNavigationLink.config(bg="white", fg="black")
            self._CarsEditing()
        elif option_selected == "reservations":
            self.ReservationsNavigationLink.config(bg="white", fg="black")
            self._ReservationsEditing()


    # Opens a frame for editing Users
    def _UsersEditing(self):
        self.AdminInterfaceMainFrame_UsersFrame.place(rely=0.12, relheight=0.88, relwidth=1.0)
        try:
            self.client_socket.send("Users:".encode())
            usersTuple = pickle.loads(self.client_socket.recv(1024))
            ScrollableContentFrame = ScrollableFrame_AdminInterface(self.AdminInterfaceMainFrame_UsersFrame, bg="purple")
            ScrollableContentFrame.place(relx=0.05, rely=0.05, relheight=0.70, relwidth=0.9)
            ScrollableContentFrame.AddUsers(usersTuple, self.client_socket)
        except ConnectionError:
            messagebox.showerror("Failed!", "Server isn't available right now, please try again later!")
            sys.exit()

    # Opens a frame for editing Cars
    def _CarsEditing(self):
        self.AdminInterfaceMainFrame_CarsFrame.place(rely=0.12, relheight=0.88, relwidth=1.0)
        self.AdminInterfaceMainFrame_CarsFrame_EditForm = Frame(self.AdminInterfaceMainFrame, bg="lightgray")
        self.AdminInterfaceMainFrame_CarsFrame_NewCarForm = Frame(self.AdminInterfaceMainFrame, bg="lightgray")
        try:
            self.client_socket.send("Cars:".encode())
            numberOfCars = int(self.client_socket.recv(1024).decode())
            listOfCars = list()
            for car in range(numberOfCars):
                listOfCars.append(pickle.loads(self.client_socket.recv(18000000)))
            ScrollableContentFrame = ScrollableFrame_AdminInterface(self.AdminInterfaceMainFrame_CarsFrame, bg="purple")
            ScrollableContentFrame.place(relx=0.05, rely=0.05, relheight=0.7, relwidth=0.55)
            ScrollableContentFrame.AddCars(listOfCars, self.client_socket)
        except ConnectionError:
            messagebox.showerror("Failed!", "Server isn't available right now, please try again later!")
            sys.exit()
        # Button for creating new Car
        buttonNewCar = Button(self.AdminInterfaceMainFrame_CarsFrame, bg="purple", fg="white", text="Create\nnew car", command=lambda :self.__createNewCar())
        buttonNewCar.place(relx=0.7, rely=0.3, relheight=0.1, relwidth=0.2)
        # Button for editing selected car
        buttonEditCar = Button(self.AdminInterfaceMainFrame_CarsFrame, bg="purple", fg="white", text="Edit Car", command=lambda :self.__editCarInfo(ScrollableContentFrame, listOfCars))
        buttonEditCar.place(relx=0.7, rely=0.6, relheight=0.1, relwidth=0.2)

    # Function that opens panel for creating a new car
    def __createNewCar(self):
        self.AdminInterfaceMainFrame_CarsFrame.place_forget()
        self.AdminInterfaceMainFrame_CarsFrame_NewCarForm.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)
        # Title
        Label(self.AdminInterfaceMainFrame_CarsFrame_NewCarForm, text="Create new car", font=("New Roman", 15, "bold"),height=3, fg="white", bg="purple").pack(fill="x")

        # Edit form
        frameForm = CarInfoForm_Frame(self.AdminInterfaceMainFrame_CarsFrame_NewCarForm, self.client_socket,bg="lightgray")
        frameForm.pack(pady=20)

        # Frame with buttons
        bottomFrame = Frame(self.AdminInterfaceMainFrame_CarsFrame_NewCarForm, bg="gray")
        bottomFrame.pack(expand=TRUE, fill="both")
        buttonReturn = Button(bottomFrame, text="<- Back", command=lambda : self.__returnToAdminMenu(self.AdminInterfaceMainFrame_CarsFrame_NewCarForm))
        buttonReturn.place(relx=0.2, relwidth=0.15, rely=0.33, relheight=0.34)
        buttonCreateCar = Button(bottomFrame, text="Create car", command=lambda: self.__createCar(self.client_socket, frameForm), bg="lightgreen")
        buttonCreateCar.place(relx=0.4, relwidth=0.2, rely=0.33, relheight=0.34)
        buttonDiscardChanges = Button(bottomFrame, text="Discard changes", command=lambda: self.__discardChanges(frameForm), bg="red")
        buttonDiscardChanges.place(relx=0.65, relwidth=0.2, rely=0.33, relheight=0.34)

    def __createCar(self, client_socket, frame):
        if len(list(filter(lambda x: x.cget("bg") == "red", frame.winfo_children()))) > 0:
            messagebox.showerror("Error",
                                 "Some of data you entered is not valid!!!\nRemember:\n\tAll entries must be filled!\n\t"
                                 "Engine Displacement, Engine Power and Price must be numbers!")
        else:
            client_socket.send("NewCar:".encode())
            client_socket.send(pickle.dumps(frame.createCarTuple()))
            a = client_socket.recv(1024).decode()
            if a == "Successful":
                messagebox.showinfo("Successful!", "You have created new car successfuly!")
            else:
                messagebox.showinfo("Error!",
                                    "There is an server error, your update attempt failed, please try again later.")

    # Function that opens panel for editing car's info
    def __editCarInfo(self, scrollableFrame, listOfCars):
        if scrollableFrame.returnSelectedCar() != None:
            self.AdminInterfaceMainFrame_CarsFrame.place_forget()
            self.AdminInterfaceMainFrame_CarsFrame_EditForm.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)
            for widget in self.AdminInterfaceMainFrame_CarsFrame_EditForm.winfo_children():
                widget.pack_forget()
            car = ""
            for car in listOfCars:
                if car[0] == scrollableFrame.returnSelectedCar():
                    car = car
                    break
            # Title
            Label(self.AdminInterfaceMainFrame_CarsFrame_EditForm, text="Edit car info", font=("New Roman", 15, "bold"), height=3, fg="white", bg="purple").pack(fill="x")

            # Edit form
            frameForm = CarInfoForm_Frame(self.AdminInterfaceMainFrame_CarsFrame_EditForm, self.client_socket, car,  bg="lightgray")
            frameForm.pack(pady=20)

            # Frame with buttons
            bottomFrame = Frame(self.AdminInterfaceMainFrame_CarsFrame_EditForm, bg="gray")
            bottomFrame.pack(expand=TRUE, fill="both")
            buttonReturn = Button(bottomFrame, text="<- Back", command=lambda : self.__returnToAdminMenu(self.AdminInterfaceMainFrame_CarsFrame_EditForm))
            buttonReturn.place(relx=0.2, relwidth=0.15, rely=0.33, relheight=0.34)
            buttonSaveChanges = Button(bottomFrame, text="Save Changes", command=lambda: self.__saveChanges(self.client_socket, frameForm, car), bg="lightgreen")
            buttonSaveChanges.place(relx=0.4, relwidth=0.2, rely=0.33, relheight=0.34)
            buttonDiscardChanges = Button(bottomFrame, text="Discard changes", command=lambda : self.__discardChanges(frameForm, car), bg="red")
            buttonDiscardChanges.place(relx=0.65, relwidth=0.2, rely=0.33, relheight=0.34)

        else:
            messagebox.showerror("Error!", "You haven't selected any car for editing!")

    # Return to Admin menu
    def __returnToAdminMenu(self, frame):
        if messagebox.askyesno("Leaving?", "Are you sure you want to return back to the main menu?"):
            frame.place_forget()
            self.AdminInterfaceMainFrame_CarsFrame.place(rely=0.12, relheight=0.88, relwidth=1.0)

    # Saving changes to database
    def __saveChanges(self, client_socket, frame, carTuple):
        if len(list(filter(lambda x: x.cget("bg") == "red", frame.winfo_children()))) > 0:
            messagebox.showerror("Error", "Some of data you entered is not valid!!!\nRemember:\n\tAll entries must be filled!\n\t"
                                          "Engine Displacement, Engine Power and Price must be numbers!")
        else:
            client_socket.send("UpdateCar:".encode())
            client_socket.send(pickle.dumps(frame.createCarTuple()))
            if client_socket.recv(1024).decode() == "Successful":
                messagebox.showinfo("Successful!", "You have updated car successfuly!")
            else:
                messagebox.showinfo("Error!", "There is an server error, your update attempt failed, please try again later.")

    # Discard changes to database
    def __discardChanges(self, frame, carTuple=None):
        if messagebox.askyesno("Confirmation?", "Are you sure you want to discard all changes and return to previous data?"):
            frame.fillEntries(carTuple) if carTuple != None else frame.fillEntries()

    # Opens a frame for editing Reservations
    def _ReservationsEditing(self):
        self.AdminInterfaceMainFrame_ReservationsFrame.place(rely=0.12, relheight=0.88, relwidth=1.0)
        list(map(lambda x: x.place_forget(), list(filter(lambda x: isinstance(x, OptionMenu), self.AdminInterfaceMainFrame_ReservationsFrame.winfo_children()))))
        # Creating scrollable frame with all reservations
        try:
            self.client_socket.send("AllReservations:".encode())
            reservations = pickle.loads(self.client_socket.recv(1024))
            self.ScrollableContentFrame = ScrollableFrame_AdminInterface(self.AdminInterfaceMainFrame_ReservationsFrame, bg="purple")
            self.ScrollableContentFrame.place(relx=0.05, rely=0.05, relheight=0.70, relwidth=0.9)
            self.ScrollableContentFrame.AddReservations(reservations, self.client_socket)
        except ConnectionError:
            messagebox.showerror("Failed!", "Server isn't available right now, please try again later!")
            sys.exit()

        # Option for filtering reservations
        Label(self.AdminInterfaceMainFrame_ReservationsFrame, text="Filter\nselection:", bg=self.AdminInterfaceMainFrame_ReservationsFrame.cget("bg")).place(relx=0.1, rely=0.83)
        self.__var = IntVar()
        filterNone = Radiobutton(self.AdminInterfaceMainFrame_ReservationsFrame, state=NORMAL, variable=self.__var, value=1, text="None", bg=self.AdminInterfaceMainFrame_ReservationsFrame.cget("bg"), command=self.__filterOptionChange)
        filterNone.place(relx=0.23, rely=0.75, relheight=0.07)
        filterUser = Radiobutton(self.AdminInterfaceMainFrame_ReservationsFrame, state=NORMAL, variable=self.__var, value=2, text="Filter by User:", bg=self.AdminInterfaceMainFrame_ReservationsFrame.cget("bg"), command=self.__filterOptionChange)
        filterUser.place(relx=0.23, rely=0.82, relheight=0.07)
        filterCar = Radiobutton(self.AdminInterfaceMainFrame_ReservationsFrame, state=NORMAL, variable=self.__var, value=3, text="Filter by Car:", bg=self.AdminInterfaceMainFrame_ReservationsFrame.cget("bg"), command=self.__filterOptionChange)
        filterCar.place(relx=0.23, rely=0.89, relheight=0.07)

        # Lists(Dictionaries) for filtering
        self.client_socket.send("Usernames:".encode())
        dictOfUsernames = dict()
        for user in pickle.loads(self.client_socket.recv(1024)):
            dictOfUsernames[user[0]] = ""
        self.__varUser = StringVar()
        self.__varUser.set("--SELECT AN USER--")

        self.client_socket.send("CarsName:".encode())
        dictOfCars = dict()
        for car in pickle.loads(self.client_socket.recv(1024)):
            dictOfCars[str(car[0]+ " " +car[1])] = ""
        self.__varCar = StringVar()
        self.__varCar.set("--SELECT A CAR--")

        # Listboxes for filtering
        self.__listboxUsers = OptionMenu(self.AdminInterfaceMainFrame_ReservationsFrame, self.__varUser, *dictOfUsernames)
        self.__listboxCars = OptionMenu(self.AdminInterfaceMainFrame_ReservationsFrame, self.__varCar, *dictOfCars)

        # Button for activating filter
        self.__buttonUseFilter = Button(self.AdminInterfaceMainFrame_ReservationsFrame, text="Activate\nfilter", bg="purple", fg="white", command=self.__filterActivation)
        self.__buttonUseFilter.place(rely=0.83, relx=0.85)

    # RadioButton change
    def __filterOptionChange(self):
        if self.__var.get() == 1:
            self.__listboxUsers.place_forget()
            self.__listboxCars.place_forget()
            self.__buttonUseFilter.config(state=DISABLED)
            self.client_socket.send("AllReservations:".encode())
            reservations = pickle.loads(self.client_socket.recv(1024))
            self.ScrollableContentFrame.AddReservations(reservations, self.client_socket)
        elif self.__var.get() == 2:
            self.__listboxUsers.place(rely=0.83, relheight=0.05, relx=0.45)
            self.__listboxCars.place_forget()
            self.__buttonUseFilter.config(state=NORMAL)
        elif self.__var.get() == 3:
            self.__listboxUsers.place_forget()
            self.__listboxCars.place(rely=0.90, relheight=0.05, relx=0.45)
            self.__buttonUseFilter.config(state=NORMAL)

    # Filter Activation
    def __filterActivation(self):
        if self.__var.get() == 2:
            if self.__varUser.get() == "--SELECT AN USER--":
                messagebox.showerror("Error!", "You didn't select any user for filtering!")
                return
            else:
                self.client_socket.send(str("ReservationsForUsername:%s" % self.__varUser.get()).encode())
        elif self.__var.get() == 3:
            if self.__varCar.get() == "--SELECT A CAR--":
                messagebox.showerror("Error!", "You didn't select any car for filtering!")
                return
            else:
                self.client_socket.send(str("ReservationsForCar:%s" % self.__varCar.get()).encode())

        reservations = pickle.loads(self.client_socket.recv(1024))
        self.ScrollableContentFrame.AddReservations(reservations, self.client_socket)

    def logOut(self):
        if messagebox.askyesno("Log out?", "Are you sure you want to log out from this account?"):
            self.currentUser = None
            self.AdminInterfaceMainFrame.pack_forget()
            self.loginFrame.pack(expand=True, fill="both")