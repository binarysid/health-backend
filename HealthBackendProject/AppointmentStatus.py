from enum import Enum

class AppointmentStatus(Enum):
    INITIATED: int = 1
    INPROGRESS: int = 2
    DONE: int = 3
    CANCELLED: int = 4