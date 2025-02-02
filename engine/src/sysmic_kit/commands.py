from enum import Enum


class Linear(Enum):
    MOVE_TO_POINT = 0
    TEST_PATH = 1
    #MOVE_SIMPLE = 2 # <- MOVE IN LINE WITHOUT OBSTACLES
    #MOVE_TO_POINT_SLOW

class Angular(Enum):
    FACE_TO_POINT = 0
    #FACE_TO_POINT_SLOW = 1

class Dribbler(Enum):
    #SPIN_SLOW = 0
    SPIN_NORMAL = 1
    #SPIN_FAST = 2
    KICK_X_GENTLE = 3
    #KICK_X_STRONG = 4
    KICK_TO_POINT = 5