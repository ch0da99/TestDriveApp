
# This is the panel where user goes after successful login as an User

from tkinter import *
from tkinter import messagebox
import pickle
from client_program.classes.Reservation_class import Reservation
from client_program.classes.User_class import User
from client_program.classes.scrollable_frame_class import ScrollableFrame, ScrollableFrame_UserInterface
from client_program.classes.registration_form_class import RegistrationForm
from tkcalendar import Calendar, DateEntry
from datetime import datetime, timedelta



class UserInterface:
    def __init__(self, parent, LoginFrame, client_socket, currentUser):
        try:
            self.parent = parent
            self.loginFrame= LoginFrame
            self.client_socket = client_socket
            self.currentUser = currentUser

            # Creating Navigation Bar
            self.UserInterfaceMainFrame = Frame(parent)
            self.UserInterfaceMainFrame.pack(expand=TRUE, fill="both")
            self.UserInterfaceMainFrame_NavigationFrame = Frame(self.UserInterfaceMainFrame, bg="orange")
            self.UserInterfaceMainFrame_NavigationFrame.place(relwidth=1.0, relheight=0.12)

            # Frame for upcoming and currently active reservations of the user
            self.upcomingReservationsNavigationLink = Button(self.UserInterfaceMainFrame_NavigationFrame, bg="white",
                                                             text="Upcoming\nreservations", font=("Arial", "11"), bd=1,
                                                             relief="groove")
            self.upcomingReservationsNavigationLink.bind("<Button-1>",
                                                         lambda x: self._navigationBarClickHandler("upcoming"))
            self.upcomingReservationsNavigationLink.place(relx=0.04, relwidth=0.2, relheight=1.0)

            # Frame for creating new reservations
            self.newReservationNavigationLink = Button(self.UserInterfaceMainFrame_NavigationFrame, bg="orange",
                                                       text="New\nreservation", font=("Arial", "11"), bd=1,
                                                       relief="groove")
            self.newReservationNavigationLink.bind("<Button-1>", lambda x: self._navigationBarClickHandler("new"))
            self.newReservationNavigationLink.place(relx=0.24, relwidth=0.2, relheight=1.0)

            # Frame for changing user informations
            self.editAccountNavigationLink = Button(self.UserInterfaceMainFrame_NavigationFrame, bg="orange",
                                                    text="Edit your\naccount", font=("Arial", "11"), bd=1,
                                                    relief="groove")
            self.editAccountNavigationLink.bind("<Button-1>", lambda x: self._navigationBarClickHandler("edit"))
            self.editAccountNavigationLink.place(relx=0.44, relwidth=0.2, relheight=1.0)

            # Label with username of the User
            self.usernameLabel = Label(self.UserInterfaceMainFrame_NavigationFrame,
                                       textvariable=StringVar(value=currentUser.username), justify=CENTER, bg="orange",
                                       font=("Arial", "14"))
            self.usernameLabel.place(relx=0.65, relwidth=0.34, relheight=0.4, rely=0.05)

            # Log out button
            self.LogOutNavigationLink = Button(self.UserInterfaceMainFrame_NavigationFrame, bg="orange", text="Log Out",
                                               font=("Arial", "11"), bd=1, relief="groove", command=lambda : self.logOut())
            self.LogOutNavigationLink.place(relx=0.72, relwidth=0.2, relheight=0.5, rely=0.5)

            # Creating references to Frame for each selection in navbar
            self.UserInterfaceMainFrame_UpcomingReservationsFrame = Frame(self.UserInterfaceMainFrame, bg="lightblue")
            self.UserInterfaceMainFrame_UpcomingReservationsFrame.place(rely=0.12, relheight=0.88, relwidth=1.0)
            self._upcomingReservationsFrameOpen()
            self.UserInterfaceMainFrame_NewReservationFrame = Frame(self.UserInterfaceMainFrame, bg="lightblue")
            self.UserInterfaceMainFrame_EditAccountFrame = Frame(self.UserInterfaceMainFrame, bg="lightblue")

            # Lists of links and frames they are reference of
            self.listOfNavigationOptions = (self.upcomingReservationsNavigationLink, self.newReservationNavigationLink, self.editAccountNavigationLink)
            self.listOfFrames = (self.UserInterfaceMainFrame_UpcomingReservationsFrame, self.UserInterfaceMainFrame_NewReservationFrame,
                                 self.UserInterfaceMainFrame_EditAccountFrame)
        except ConnectionError:
            messagebox.showerror("Failed!", "Server isn't available right now, please try again later!")
            sys.exit()


    # Function that handles switching through the navbar links
    def _navigationBarClickHandler(self, option_selected):
        list(map(lambda x: x.config(bg="orange"), self.listOfNavigationOptions))
        list(map(lambda x: x.place_forget(), self.listOfFrames))
        if option_selected == "upcoming":
            self.upcomingReservationsNavigationLink.config(bg="white")
            self._upcomingReservationsFrameOpen()
        elif option_selected == "new":
            self.newReservationNavigationLink.config(bg="white")
            self._newReservationFrameOpen()
        elif option_selected == "edit":
            self.editAccountNavigationLink.config(bg="white")
            self._editAccountFrameOpen()

    # Opens frame for Upcoming and current reservations
    def _upcomingReservationsFrameOpen(self):
        self.UserInterfaceMainFrame_UpcomingReservationsFrame.place(rely=0.12, relheight=0.88, relwidth=1.0)
        self.UserInterfaceMainFrame_UpcomingReservationsFrame_ContentFrame = Frame(self.UserInterfaceMainFrame_UpcomingReservationsFrame)
        self.UserInterfaceMainFrame_UpcomingReservationsFrame_ContentFrame.place(relheight=0.7, relwidth=0.9, relx=0.05, rely=0.1)
        self.buttonDeleteAllUserReservations = Button(self.UserInterfaceMainFrame_UpcomingReservationsFrame, text="Delete all\nreservations",
                                                      command=lambda:self._deletingAllReservations())
        self.buttonDeleteAllUserReservations.place(rely=0.85, relheight=0.1, relx=0.4, relwidth=0.2)
        try:
            self.client_socket.send(str("Reservations:%s" % self.currentUser.id).encode())
            resultFromDatabase = pickle.loads(self.client_socket.recv(1024))
            listOfReservationsForUserFrame = ScrollableFrame_UserInterface(self.UserInterfaceMainFrame_UpcomingReservationsFrame_ContentFrame)
            listOfReservationsForUserFrame.pack(expand=TRUE, fill="both")
            listOfReservationsForUserFrame.addReservationsForUser(resultFromDatabase, self.client_socket)
        except ConnectionError:
            messagebox.showerror("Failed!", "Server isn't available right now, please try again later!")
            sys.exit()

    # Delete all reservations for this User
    def _deletingAllReservations(self):
        if messagebox.askquestion("Delete ALL reservations!?","Do you really want to delete all of your reservations?"):
            if messagebox.askyesnocancel("Are you sure?", "Once you delete all of your current reservations you can't retrieve them.\nProceed?"):
                self.client_socket.send(str("DeleteAllReservationsForUser:%d" % self.currentUser.id).encode())

    # Opens a frame for creating sew reservations
    def _newReservationFrameOpen(self):
        self.UserInterfaceMainFrame_NewReservationFrame.place(rely=0.12, relheight=0.88, relwidth=1.0)
        UserInterfaceMainFrame_NewReservationFrame_ContentFrame = Frame(self.UserInterfaceMainFrame_NewReservationFrame)
        UserInterfaceMainFrame_NewReservationFrame_ContentFrame.place(relx=0.01, relwidth=0.59, rely=0.05, relheight=0.8)
        try:
            self.client_socket.send("Cars:".encode())
            numberOfCars = int(self.client_socket.recv(1024).decode())
            listOfCars = list()
            for car in range(numberOfCars):
                listOfCars.append(pickle.loads(self.client_socket.recv(18*1024*1024)))
            carsListScrollableFrame = ScrollableFrame_UserInterface(UserInterfaceMainFrame_NewReservationFrame_ContentFrame)
            carsListScrollableFrame.addCars(listOfCars, self.client_socket)
            carsListScrollableFrame.pack(expand=TRUE, fill="both")
        except ConnectionResetError:
            messagebox.showerror("Failed!", "Server isn't available right now, please try again later!")
            sys.exit()

        Label(self.UserInterfaceMainFrame_NewReservationFrame, text="Select pick-up date:", bg="orange").place(relx=0.62, relwidth=0.36, rely=0.06, relheight=0.04)
        self.pickUpDateEntry = DateEntry(self.UserInterfaceMainFrame_NewReservationFrame)
        self.pickUpDateEntry.place(relx=0.62, relwidth=0.36, rely=0.1, relheight=0.1)
        Label(self.UserInterfaceMainFrame_NewReservationFrame, text="Drop off date will automatically\n be set 2 days after car has been\n reserved for picking up"
                                                                    "\n- - - - - - - - - - - - \nPlease return car in 48h!", bg="orange")\
            .place(relx=0.62, relwidth=0.36, rely=0.26, relheight=0.20)
        self.buttonCreateNewReservation = Button(self.UserInterfaceMainFrame_NewReservationFrame, bg="darkorange", text="Create new\nreservation", command=self.__createNewReservation, font=("New Roman",13))
        self.buttonCreateNewReservation.place(relx=0.7, relwidth=0.19, rely=0.5, relheight=0.1)

    # Function that creates new reservations with all parameters
    def __createNewReservation(self):
        if not ScrollableFrame_UserInterface.returnSelectedCar():
            messagebox.showerror("Error!", "You didn't select any car to create reservation!")
            return
        elif (self.pickUpDateEntry.get_date() - datetime.date(datetime.now())).days < 0:
            messagebox.showerror("Error", "You can't set pick-up date to day that has already passed!")
            return
        else:
            try:
                self.client_socket.send(str("ReservationsOfCar:%s" % ScrollableFrame_UserInterface.returnSelectedCar()).encode())
                tuplesReservation = pickle.loads(self.client_socket.recv(1024))
                reservationsOfThisCar = list()
                for reservation in tuplesReservation:
                    reservationsOfThisCar.append(Reservation.tupleConstructor(reservation))
                overrideReservations = list(filter(self.__isOverriden, reservationsOfThisCar))
                if len(overrideReservations) > 0:
                    message = "Unfortunately we are unable to reserve you this car for the date you have chosen because " \
                              "it's already reserved by another user:"
                    for reservation in overrideReservations:
                        message += "\n" + str(reservation.pickUpDate.day) + "." + str(reservation.pickUpDate.month) + "." + str(reservation.pickUpDate.year) + "."\
                                   + " - " + str(reservation.dropOffDate.day) + "." + str(reservation.dropOffDate.month) + "." + str(reservation.dropOffDate.year) + "."
                    messagebox.showerror("Error!", message)
                else:
                    newReservation = Reservation("", int(ScrollableFrame_UserInterface.returnSelectedCar()), self.currentUser.id,
                                                 self.pickUpDateEntry.get_date(), self.pickUpDateEntry.get_date() + timedelta(days=2))
                    self.client_socket.send("NewReservation:".encode())
                    self.client_socket.send(pickle.dumps(newReservation.toTuple()))
                    if self.client_socket.recv(1024).decode() == "Successful":
                        messagebox.showinfo("Successful!", "You successfuly added new reservation!")
            except ConnectionError:
                messagebox.showerror("Failed!", "Server isn't available right now, please try again later!")
                sys.exit()
    # Function that checks if selected dates for new reservations
    # override fully or partly any other reservations for that car
    def __isOverriden(self, reservation):
        if reservation.pickUpDate >= self.pickUpDateEntry.get_date() + timedelta(days=2) or reservation.dropOffDate <= self.pickUpDateEntry.get_date():
            return False
        else:
            return True

    # Opens a frame for changing personal info of the current user
    def _editAccountFrameOpen(self):
        self.UserInterfaceMainFrame_EditAccountFrame.place(rely=0.12, relheight=0.88, relwidth=1.0)
        frameEditAccount = RegistrationForm(self.UserInterfaceMainFrame_EditAccountFrame, self.client_socket, self.currentUser)
        frameEditAccount.config(bg="lightblue")
        frameEditAccount.place(relheight=0.7, relwidth=1.0, rely=0.05)
        frameEditAccount.setEntries(frameEditAccount.listOfEntries)
        btnConfirmChanges = Button(self.UserInterfaceMainFrame_EditAccountFrame, bg="lightgreen", text="Confirm changes", command=lambda: self.__confirmChangesOfAccInfo(frameEditAccount))
        btnConfirmChanges.place(rely=0.79, relheight=0.1, relx=0.2, relwidth=0.2)
        btnDiscardChanges = Button(self.UserInterfaceMainFrame_EditAccountFrame,  bg="red", text="Discard changes", command=lambda: self.__discardChangesOfAccInfo(frameEditAccount))
        btnDiscardChanges.place(rely=0.79, relheight=0.1, relx=0.65, relwidth=0.2)

    # Confirmation of acc info changes in messagebox
    def __confirmChangesOfAccInfo(self, frame):
        if len(list(filter(lambda x: x.cget("bg") != "lightgreen", frame.listOfEntries))) == 0:
            if messagebox.askquestion("Change personal info?", "Do you really want to change your personal info?"):
                try:
                    self.client_socket.send(str(("ChangeUserInfo:%d") % int(self.currentUser.id)).encode())
                    self.client_socket.send(
                        pickle.dumps(User("", frame.entryFirstName.get(), frame.entryLastName.get(), frame.entryUsername.get(),
                                          frame.entryEmail.get(), frame.entryPhoneNumber.get(),  frame.entryPassword.get(), "No").toTuple()))
                    if self.client_socket.recv(1024).decode() == "Successful":
                        messagebox.showinfo("Successful!", "Your personal info has been changed successfuly!")
                        frame.setEntries(frame.listOfEntries)
                        frame.entryConfirmPassword.config(textvariable=StringVar())
                except ConnectionResetError:
                    messagebox.showerror("Failed!", "Server isn't available right now, please try again later!")
                    sys.exit()
        else:
            messagebox.showerror("Error!", "Entries can't be empty or with invalid data!")

    def __discardChangesOfAccInfo(self, frame):
        if messagebox.askyesno("Are you sure?", "Are you sure you want to discard all of changes you've made?"):
            frame.setEntries(frame.listOfEntries)


    # Function for logging out of account
    def logOut(self):
        if messagebox.askyesno("Log out?", "Are you sure you want to log out from this account?"):
            self.currentUser = None
            self.UserInterfaceMainFrame.pack_forget()
            self.loginFrame.pack(expand=True, fill="both")



