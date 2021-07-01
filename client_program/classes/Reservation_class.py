
# prototype for an instance of Reservation created by User

class Reservation:
    def __init__(self, id=None, carId=None, userId=None, pickUpDate=None, dropOffDate=None):
        self.id = id
        self.carId = carId
        self.userId = userId
        self.pickUpDate = pickUpDate
        self.dropOffDate = dropOffDate
        #self.price = abs((datetime.strptime(dropOffDate, "%Y-%m-%d") - (datetime.strptime(pickUpDate, "%Y-%m-%d"))).days)

    @staticmethod
    def tupleConstructor(tupleReservation):
        if tupleReservation is not None:
            return Reservation(tupleReservation[0], tupleReservation[1], tupleReservation[2], tupleReservation[3], tupleReservation[4])
        else:
            return Reservation()

    def toTuple(self):
        return self.id, self.carId, self.userId, self.pickUpDate, self.dropOffDate


