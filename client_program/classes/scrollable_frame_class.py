
# This is custom made Frame that can be scrolled verticaly

from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
import pickle
from client_program.classes.Car_class import Car
from client_program.classes.Reservation_class import Reservation
from client_program.classes.User_class import User
from datetime import datetime
from functools import reduce

# container for different types of Frame-data objects
class ScrollableFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, master=parent)
        self.parent = parent

        # Canvas for connecting scrollbar with
        self.canvas = Canvas(self, width=50)
        self.canvas.pack(side=LEFT, expand=TRUE, fill="both")

        # Container for other frames
        self.scrollFrame = Frame(self)

        # Scrollbar
        self.yScrollbar = Scrollbar(self, command=self.canvas.yview, orient=VERTICAL)
        self.yScrollbar.pack(side=LEFT, fill="both")

        # Creating scrollable window
        self.canvas.create_window((0, 0), window=self.scrollFrame, anchor='nw')
        self.canvas.config(yscrollcommand=self.yScrollbar.set)
        self.canvas.bind("<Configure>", lambda x: self.canvas.config(scrollregion=self.canvas.bbox("all")))



    def _removingAllChildrenFrames(self):
        for frame in self.scrollFrame.winfo_children():
            frame.pack_forget()

# child class of ScrollableFrame with methods for Scrollable frames in User Interface
class ScrollableFrame_UserInterface(ScrollableFrame):
    def __init__(self, parent, *args, **kwargs):
        ScrollableFrame.__init__(self, parent, *args, **kwargs)

    # Appending reservations of an user // Upcoming Reservations frame
    def addReservationsForUser(self, listOfReservations, client_socket):
        self._removingAllChildrenFrames()
        for reservation in listOfReservations:
            frame = ReservationFrameForUserInterface(self.scrollFrame, reservation, client_socket, bg="gray", width=10, padx=3, border=3)
            frame.pack(pady=3)

    # Appending cars // New Reservation
    def addCars(self, listOfCars, client_socket):
        self._removingAllChildrenFrames()
        CarFrameForUserInterface.listOfCarFrames.clear()
        self.config(width=200)
        for car in listOfCars:
            frame = CarFrameForUserInterface(self.scrollFrame, car, client_socket, width=40)
            frame.pack(pady=3)
            CarFrameForUserInterface.listOfCarFrames.append(frame)

    # Returns selected car's ID
    @staticmethod
    def returnSelectedCar():
        for carFrame in CarFrameForUserInterface.listOfCarFrames:
            if carFrame.cget("bg") == "green":
                return carFrame.widgetName

# child class of ScrollableFrame with methods for Scrollable frames in User Interface
class ScrollableFrame_AdminInterface(ScrollableFrame):
    def __init__(self, parent, *args, **kwargs):
        ScrollableFrame.__init__(self, parent, *args, **kwargs)

    def AddUsers(self, tupleUsers, client_socket):
        self._removingAllChildrenFrames()
        for user in tupleUsers:
            frame = UserFrameForAdminInterface(self.scrollFrame, user, client_socket, width=430, height=90, bg="lightgray")
            frame.pack(pady=3)

    def AddCars(self, tupleCars, client_socket):
        self._removingAllChildrenFrames()
        for car in tupleCars:
            frame = CarFrameForAdminInterface(self.scrollFrame, car, client_socket, height=90, bg="lightgray")
            frame.pack(pady=3)

    def AddReservations(self, tupleReservations, client_socket):
        self._removingAllChildrenFrames()
        for reservation in tupleReservations:
            frame = ReservationFrameForAdminInterface(self.scrollFrame, reservation, client_socket, height=90, bg="lightgray")
            frame.pack(pady=3)

    def returnSelectedCar(self):
        for frame in self.scrollFrame.winfo_children():
            if frame.cget("bg") == "green":
                return frame.widgetName


# label that contains image of car
class CarImageLabel(Label):
    def __init__(self, parent, binaryPicture, *args, **kwargs):
        Label.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Transformation from BLOB file to Image
        imgBytes = Image.open(BytesIO(binaryPicture))
        imgBytes.thumbnail((100, 100))
        img = ImageTk.PhotoImage(imgBytes)
        self.config(image=img)
        self.image = img


# frame that contains a single reservation's info
class ReservationFrameForUserInterface(Frame):
    def __init__(self, parent, tupleReservation, client_socket, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        try:
            # image of reserved car
            client_socket.send(("CarInfo:%s" % tupleReservation[1]).encode())
            carInfo = pickle.loads(client_socket.recv(17000000))
            carImgLabel = CarImageLabel(self, carInfo[1])
            carImgLabel.pack(side=LEFT)

            # panel with info of reservation
            infoPanel = Frame(self, width=30)
            infoPanel.pack(side=LEFT, padx=40)
            labelCar = Label(infoPanel, text=str("%s %s" % (carInfo[2], carInfo[3])))
            labelCar.pack(side=TOP)
            labelPickUpDate = Label(infoPanel, text=str("Pick-up date: %s.%s.%s." % (
            tupleReservation[3].day, tupleReservation[3].month, tupleReservation[3].year)))
            labelPickUpDate.pack(side=TOP)
            labelDropOffDate = Label(infoPanel, text=str("Drop-off date: %s.%s.%s." % (
            tupleReservation[4].day, tupleReservation[4].month, tupleReservation[4].year)))
            labelDropOffDate.pack(side=TOP)

            # button for deleting particular reservation
            buttonDelete = Button(self, text="Delete\nreservation",
                                  command=lambda: self._deleteReservation(client_socket, tupleReservation[0]))
            buttonDelete.pack(side=LEFT, padx=20)
        except ConnectionError:
            messagebox.showerror("Failed!", "Server isn't available right now, please try again later!")
            sys.exit()



    def _deleteReservation(self, client_socket, idInDatabase):
        client_socket.send(str("DeleteReservation:%s" % idInDatabase).encode())
        if client_socket.recv(1024).decode() == "Successful":
            messagebox.showinfo("Successful!", "Reservation successfuly deleted!")
            self.pack_forget()

# frame that contains information about a car
class CarFrameForUserInterface(Frame):
    listOfCarFrames = list()
    selectedCar = None

    def __init__(self, parent, tupleCar, client_socket, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        car = Car()
        car = car.tupleConstructor(tupleCar)
        self.widgetName = car.id
        try:
            # image of car
            self.carImgLabel = CarImageLabel(self, tupleCar[1], cursor="hand2")
            self.carImgLabel.pack(side=LEFT)
            self.carImgLabel.bind("<Button-1>", lambda x:self.selectingACar())

            # car information and characteristics
            self.labelCarInfo = Label(self, cursor="hand2", justify=LEFT, text=str("%s %s  -  %s euros\n\nEngine power: %s horse power\nEngine displacement: %scc\nCar body: %s" %
                                                (car.manufacturer, car.model, car.price, car.engine_power, car.engine_displacement, car.car_body)))
            self.labelCarInfo.pack(side=LEFT, padx=1)
            self.labelCarInfo.bind("<Button-1>", lambda x: self.selectingACar())
        except ConnectionError:
            messagebox.showerror("Failed!", "Server isn't available right now, please try again later!")
            sys.exit()



    def selectingACar(self):
        self.selectedCar = self.widgetName
        for frame in self.listOfCarFrames:
            frame.config(bg="white")
            frame.carImgLabel.config(bg="white")
            frame.labelCarInfo.config(bg="white")
        self.config(bg="green")
        self.carImgLabel.config(bg="green")
        self.labelCarInfo.config(bg="green")


# frame that contains info of a user
class UserFrameForAdminInterface(Frame):
    def __init__(self, parent, tupleUser, client_socket, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        user = User.tupleConstructor(tupleUser)

        # Labels with information about user
        Label(self, text=str("%s " % user.username), bg=self.cget("bg"), font=("New Roman", "18", "bold")).place(relx=0.0, rely=0.05, relheight=0.30, relwidth=0.6)
        Label(self, text="ADMIN" if user.admin == "Yes" else "USER", bg=self.cget("bg"), fg="Red" if user.admin == "Yes" else "Green",
              font=("New Roman", "13", "bold"), justify=LEFT).place(relx=0.60, rely=0.05, relheight=0.4, relwidth=0.15)
        Label(self, text=str("Full Name: %s %s" % (user.firstName, user.lastName)), bg=self.cget("bg"), justify=LEFT).place(rely=0.40, relx=0.05, relheight=0.2, relwidth=0.5)
        Label(self, text=str("Phone number: %s" % user.phone), bg=self.cget("bg"), justify=LEFT).place(rely=0.60, relx=0.05, relheight=0.2, relwidth=0.5)
        Label(self, text=str("Email: %s" % user.email), bg=self.cget("bg"), justify=LEFT).place(rely=0.80, relx=0.05, relheight=0.2, relwidth=0.5)
        self.__lblPassword = Label(self, text=str("Password: %s" % "".join(list(map(lambda x: "*", list(user.password))))), bg=self.cget("bg"), justify=LEFT)
        self.__lblPassword.place(rely=0.45, relx=0.5, relheight=0.2, relwidth=0.4)
        self.__lblShowHide = Label(self, text="Show password", fg="blue", bg=self.cget("bg"), cursor="hand2")
        self.__lblShowHide.place(rely=0.65, relx=0.5, relheight=0.2, relwidth=0.4)
        self.__lblShowHide.bind("<Button-1>", lambda x: self.__showHidePassword(user))

        # Button for deleting user
        if user.admin == "No":
            btnDeleteUser = Button(self, text="Delete user", bg="pink", font=("New Roman", 13, "bold"), cursor="hand2", command=lambda: self.__deleteUser(user, client_socket))
            btnDeleteUser.place(relx=0.77, rely=0.05, relheight=0.4, relwidth=0.23)


    # Function that hides and shows password
    def __showHidePassword(self, user):
        if re.match("Show*", self.__lblShowHide.cget("text")):
            self.__lblShowHide.config(text="Hide password")
            self.__lblPassword.config(text="Password: %s" % user.password)
        else:
            self.__lblShowHide.config(text="Show password")
            self.__lblPassword.config(text=str("Password: %s" % "".join(list(map(lambda x: "*", list(user.password))))))

    # Function that deletes user
    def __deleteUser(self, user, client_socket):
        if messagebox.askquestion("Confirmation?", str("Are you sure you want to delete user '%s'?\n"
                                                       "Once you did, all of the reservations that he/she created will be automatically deleted." % user.username)):
            client_socket.send(str("DeleteUser:%s" % user.id).encode())
            if client_socket.recv(1024).decode() == "Successful":
                messagebox.showinfo("Successful!", str("You successfuly deleted user '%s' and all reservations connected with that account." % user.username))
                self.pack_forget()
            else:
                messagebox.showerror("Error!", "System is currently unable to delete selected user, try again later!")

# frame that contains info of a reservation
class ReservationFrameForAdminInterface(Frame):
    def __init__(self, parent, tupleReservation, client_socket, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        reservation = Reservation.tupleConstructor(tupleReservation)
        self.widgetName = reservation.id

        # Getting user and a car that are associated with this reservation
        client_socket.send(str("CarInfo:%s" % reservation.carId).encode())
        car = Car.tupleConstructor(pickle.loads(client_socket.recv(18000000)))
        client_socket.send(str("UserInfo:%s" % reservation.userId).encode())
        user = User.tupleConstructor(pickle.loads(client_socket.recv(1024)))

        # Image of the car
        image = CarImageLabel(self, car.image, cursor="hand2")
        image.pack(side=LEFT)

        # car name, username, pick-up and drop-off date, price
        infoFrame = Frame(self, bg=self.cget("bg"), width=320, height=90)
        infoFrame.pack(side=LEFT)
        Label(infoFrame, text="Car:", bg=self.cget("bg"), font=("New Roman", "10"), justify=RIGHT)\
            .place(relx=0.0, rely=0.0, relheight=0.3)
        Label(infoFrame, text=str("%s %s" % (car.manufacturer, car.model)), bg=self.cget("bg"), font=("New Roman", "13", "bold"), justify=LEFT)\
            .place(relx=0.1, rely=0.0, relheight=0.3)
        Label(infoFrame, text="User:", bg=self.cget("bg"), font=("New Roman", "10"), justify=RIGHT)\
            .place(relx=0.0, rely=0.3, relheight=0.3)
        Label(infoFrame, text=str("%s" % user.username), fg="blue", bg=self.cget("bg"), font=("New Roman", "11", "bold"), justify=LEFT)\
            .place(relx=0.1, rely=0.3, relheight=0.3)
        Label(infoFrame, text="Pick-up date:", bg=self.cget("bg")) \
            .place(relx=0.6, relwidth=0.35, rely=0, relheight=0.15)
        Label(infoFrame, text=str("%s.%s.%s" % (reservation.pickUpDate.day, reservation.pickUpDate.month, reservation.pickUpDate.year)), bg=self.cget("bg"), font=("New Roman", 10,"bold")) \
            .place(relx=0.6, relwidth=0.35, rely=0.15, relheight=0.15)
        Label(infoFrame, text="Drop-off date:", bg=self.cget("bg")) \
            .place(relx=0.6, relwidth=0.35, rely=0.35, relheight=0.15)
        Label(infoFrame, text=str("%s.%s.%s" % (reservation.dropOffDate.day, reservation.dropOffDate.month, reservation.dropOffDate.year)), bg=self.cget("bg"), font=("New Roman", 10,"bold")) \
            .place(relx=0.6, relwidth=0.35, rely=0.5, relheight=0.15)
        Label(infoFrame, text="Price:", bg=self.cget("bg")) \
            .place(relx=0.7, relwidth=0.1, rely=0.65, relheight=0.35)
        Label(infoFrame, text=str("%se" % car.price), bg=self.cget("bg"), font=("New Roman", 10,"bold")) \
            .place(relx=0.8, rely=0.65, relheight=0.35)

        # Button for deleting a reservation
        btnDeleteReservation = Button(infoFrame, text="Delete reservation", bg="pink", font=("New Roman", 12, "bold"), command=lambda :self.__deleteReservation(client_socket))
        btnDeleteReservation.place(rely=0.65, relheight=0.3, relx=0.05, relwidth=0.45)


    def __deleteReservation(self, client_socket):
        if messagebox.askquestion("Confirmation?", "Are you sure you want to delete this reservation?"):
            client_socket.send(str("DeleteReservation:%s" % self.widgetName).encode())
            if client_socket.recv(1024).decode() == "Successful":
                self.pack_forget()
                messagebox.showinfo("Successful", "The reservation has been deleted successfuly.")

# frame that contains info of a car
class CarFrameForAdminInterface(Frame):
    selectedCar = None

    def __init__(self, parent, tupleCar, client_socket, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        car = Car.tupleConstructor(tupleCar)
        self.widgetName = car.id

        # Image of the car
        image = CarImageLabel(self, car.image, cursor="hand2")
        image.pack(side=LEFT)

        # all other informations about car
        infoFrame = Frame(self, width=150, height=80, bg="lightgray", cursor="hand2")
        infoFrame.pack(side=LEFT)
        Label(infoFrame, text=str("%s %s" % (car.manufacturer, car.model)), font=("New Roman", 13, "bold"), bg="lightgray").place(relx=0.0, rely=0.0, relheight=0.3, relwidth=1.0)
        Label(infoFrame, text=str("Engine displacement: %scc" % car.engine_displacement), bg="lightgray").place(relx=0.0, rely=0.3, relheight=0.15, relwidth=1.0)
        Label(infoFrame, text=str("Engine power: %s hp" % car.engine_power), bg="lightgray").place(relx=0.0, rely=0.45, relheight=0.15, relwidth=1.0)
        Label(infoFrame, text=str("Car body: %s" % car.car_body), bg="lightgray").place(relx=0.0, rely=0.6, relheight=0.15, relwidth=1.0)
        Label(infoFrame, text=str("Price: %s" % car.price), bg="lightgray").place(relx=0.0, rely=0.75, relheight=0.25, relwidth=1.0)

        for widget in self.winfo_children():
            widget.bind("<Button-1>", lambda x: self.__selectingACar(parent))
            for subwidget in widget.winfo_children():
                subwidget.bind("<Button-1>", lambda x: self.__selectingACar(parent))

    def __selectingACar(self, parent):
        for frame in parent.winfo_children():
            for widget in frame.winfo_children():
                widget.config(bg="lightgray")
                for subwidget in widget.winfo_children():
                    subwidget.config(bg="lightgray")
            frame.config(bg="lightgray")
        self.config(bg="green")
        for widget in self.winfo_children():
            widget.config(bg="green")
            for subwidget in widget.winfo_children():
                subwidget.config(bg="green")