from botbuilder.schema import Attachment


class UserProfile:

    def __init__(self, name: str = None, shape: str = None, color: str = None, time: str = None, date: str = None, health: str =  None, type: str = None, initial: int = 0, picture: Attachment = None):
        self.name = name
        self.health = health
        self.color = color
        self.shape = shape
        self.time = time
        self.date = date
        self.type = type
        self.initial = initial
        self.picture = picture
