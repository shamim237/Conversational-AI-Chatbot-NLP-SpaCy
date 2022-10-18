from botbuilder.schema import Attachment


class UserProfile:

    def __init__(self,  shape: str = None, time: str = None, date: str = None,  type: str = None, initial: int = 0, picture: Attachment = None):
        self.shape = shape
        self.time = time
        self.date = date
        self.type = type
        self.initial = initial
        self.picture = picture
