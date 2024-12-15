import time

class PID:

    def __init__(self, kP, kI, set_point):
        self.kP = kP
        self.kI = kI
        self.last_time = time.time()
        self.set_point = set_point
        self.i = 0


    def compute(self, measurement):
        

        error = self.set_point - measurement
        p = self.kP*error
        self.i = self.i + self.kI*error*(time.time() - self.last_time)


        self.last_time = time.time()

        pi = p + self.i
        return pi