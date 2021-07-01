
# Prototype for row in table Cars of database TestDriveDatabase

class Car:
    def __init__(self, id=None, image=None, manufacturer=None, model=None, engine_power=None, engine_displacement=None,
                 car_body=None, price=None):
        self.id = id
        self.image = image
        self.manufacturer = manufacturer
        self.model = model
        self.engine_power = engine_power
        self.engine_displacement = engine_displacement
        self.car_body = car_body
        self.price = price

    @classmethod
    def tupleConstructor(cls, tupleCar):
        if tupleCar is not None:
            return Car(tupleCar[0], tupleCar[1], tupleCar[2], tupleCar[3], tupleCar[4], tupleCar[5],
                       tupleCar[6], tupleCar[7])
        else:
            return Car()

    def toTuple(self):
        return self.id, self.image, self.manufacturer, self.model, self.engine_power, \
               self.engine_displacement, self.car_body, self.price