
# Prototype for row in table Users of database TestDriveDatabase

class User:
    def __init__(self, id=None, firstName=None, lastName=None, username=None, email=None, phone=None, password=None, admin=None):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.username = username
        self.email = email
        self.phone = phone
        self.password = password
        self.admin = admin

    @classmethod
    def tupleConstructor(cls, tupleUser):
        if tupleUser is not None:
            return User(tupleUser[0], tupleUser[1], tupleUser[2], tupleUser[3], tupleUser[4], tupleUser[5],
                        tupleUser[6], tupleUser[7])
        else:
            return User()

    def toTuple(self):
        return self.id, self.firstName, self.lastName, self.username,  self.email, self.phone, self.password, self.admin

