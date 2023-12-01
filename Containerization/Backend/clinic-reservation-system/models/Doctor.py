
class Doctor:

    def __call__(self, name, password):
        self.getName()
        self.getPassword()
        self.setName(name)
        self.setPassword(password)

    def __init__(self):
        self.name = None
        self.password = None
        self.doctorID = None
        self.email = None

    def setName(self, name):
        self.name = name

    def setID(self, doctorID):
        self.doctorID = doctorID

    def setEmail(self, email):
        self.email = email

    def setPassword(self, password):
        self.password = password

    def getName(self):
        return self.name

    def getID(self):
        return self.doctorID

    def getEmail(self):
        return self.email

    def getPassword(self):
        return self.password
