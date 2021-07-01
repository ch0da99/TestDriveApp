
# This class is created for purpose of adding new car or changing
# info of an existing one

from tkinter import *
from client_program.classes.Car_class import Car
from client_program.classes.scrollable_frame_class import CarImageLabel
from tkinter import filedialog
from PIL import ImageTk, Image

class CarInfoForm_Frame(Frame):
    def __init__(self, parent, client_socket, carTuple = None, *args, **kwargs):
        Frame.__init__(self, master=parent, *args, **kwargs)
        self.widgetName = carTuple[0] if carTuple != None else ""


        self.varManufacturer = StringVar()
        self.varModel = StringVar()
        self.varEngineDisplacement = StringVar()
        self.varEnginePower = StringVar()
        self.varCarBody = StringVar()
        self.varPrice = StringVar()


        buttonSelectImage = Button(self, text="Select image of the car", command=lambda :self.__imageSelect(labelImage))
        buttonSelectImage.grid(row=0, column=0, sticky="e", ipadx=10)
        labelImage = Label(self) if carTuple == None else CarImageLabel(self, carTuple[1])
        labelImage.grid(row=0, column=1, sticky="w", pady=5, padx=10)
        self.imageAsBLOB = "" if carTuple == None else carTuple[1]

        Label(self, text="Car manufacturer:", bg=parent.cget("bg"), font=("New Roman", 11)).grid(row=1, column=0, sticky="e", ipadx=10)
        entryManufacturer = Entry(self, textvariable=self.varManufacturer)
        entryManufacturer.widgetName = "entryManufacturer"
        entryManufacturer.bind("<FocusOut>", lambda x: self.__validationOfEntries(entryManufacturer))
        entryManufacturer.grid(row=1, column=1, sticky="w", pady=5, padx=10)

        Label(self, text="Car model:", bg=parent.cget("bg"), font=("New Roman", 11)).grid(row=2, column=0, sticky="e", ipadx=10)
        entryModel = Entry(self, textvariable=self.varModel)
        entryModel.widgetName = "entryModel"
        entryModel.bind("<FocusOut>", lambda x: self.__validationOfEntries(entryModel))
        entryModel.grid(row=2, column=1, sticky="w", pady=5, padx=10)

        Label(self, text="Engine displacement:", bg=parent.cget("bg"), font=("New Roman", 11)).grid(row=3, column=0, sticky="e", ipadx=10)
        entryEngineDisplacement = Entry(self, textvariable=self.varEngineDisplacement)
        entryEngineDisplacement.widgetName = "entryEngineDisplacement"
        entryEngineDisplacement.bind("<FocusOut>", lambda x: self.__validationOfEntries(entryEngineDisplacement))
        entryEngineDisplacement.grid(row=3, column=1, sticky="w", pady=5, padx=10)

        Label(self, text="Engine power:", bg=parent.cget("bg"), font=("New Roman", 11)).grid(row=4, column=0, sticky="e", ipadx=10)
        entryEnginePower = Entry(self, textvariable=self.varEnginePower)
        entryEnginePower.widgetName = "entryEnginePower"
        entryEnginePower.bind("<FocusOut>", lambda x: self.__validationOfEntries(entryEnginePower))
        entryEnginePower.grid(row=4, column=1, sticky="w", pady=5, padx=10)

        Label(self, text="Car body:", bg=parent.cget("bg"), font=("New Roman", 11)).grid(row=5, column=0, sticky="e", ipadx=10)
        entryCarBody = Entry(self, textvariable=self.varCarBody)
        entryCarBody.widgetName = "entryCarBody"
        entryCarBody.bind("<FocusOut>", lambda x: self.__validationOfEntries(entryCarBody))
        entryCarBody.grid(row=5, column=1, sticky="w", pady=5, padx=10)

        Label(self, text="Price:", bg=parent.cget("bg"), font=("New Roman", 11)).grid(row=6, column=0, sticky="e", ipadx=10)
        entryPrice = Entry(self, textvariable=self.varPrice)
        entryPrice.widgetName = "entryPrice"
        entryPrice.bind("<FocusOut>", lambda x: self.__validationOfEntries(entryPrice))
        entryPrice.grid(row=6, column=1, sticky="w", pady=5, padx=10)

        # Checking if this is option for editing and if it is
        # filling entries with information about the car
        if carTuple != None:
            self.fillEntries(carTuple)



    def __imageSelect(self, label):
        imagePath = filedialog.askopenfilename(initialdir="c:/Users/HP/Desktop/CarPictures", title="Select car image")
        if imagePath != "":
            imageBytes = Image.open(imagePath)
            imageBytes.thumbnail((100,100))
            image = ImageTk.PhotoImage(imageBytes)
            label.config(image=image)
            label.image = image
            self.__photoToBLOB(imagePath)

    def __photoToBLOB(self, imagePath):
        with open(imagePath, "rb") as f:
            self.imageAsBLOB = f.read()

    def fillEntries(self, carTuple = None):
        if carTuple != None:
            car = Car.tupleConstructor(carTuple)
            self.varManufacturer.set(car.manufacturer)
            self.varModel.set(car.model)
            self.varEngineDisplacement.set(car.engine_displacement)
            self.varEnginePower.set(car.engine_power)
            self.varCarBody.set(car.car_body)
            self.varPrice.set(car.price)

            for widget in self.winfo_children():
                if isinstance(widget, Entry):
                    widget.config(bg="lightgreen")
        else:
            self.varManufacturer.set("")
            self.varModel.set("")
            self.varEngineDisplacement.set("")
            self.varEnginePower.set("")
            self.varCarBody.set("")
            self.varPrice.set("")



    def __validationOfEntries(self, entry):
        entry.config(bg="lightgreen")
        if entry.get() == "":
            entry.config(bg="red")
        if entry.widgetName == "entryEngineDisplacement" or entry.widgetName == "entryEnginePower" or entry.widgetName == "entryPrice":
            if not entry.get().isdigit():
                entry.config(bg="red")

    def createCarTuple(self):
        return self.widgetName, self.imageAsBLOB, self.varManufacturer.get(), self.varModel.get(), \
               self.varEngineDisplacement.get(), self.varEnginePower.get(), self.varCarBody.get(), self.varPrice.get()







