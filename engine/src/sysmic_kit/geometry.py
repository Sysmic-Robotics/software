import math

class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        raise TypeError("Operand must be an instance of Vector2")

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        raise TypeError("Operand must be an instance of Vector2")

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vector2(self.x * scalar, self.y * scalar)
        raise TypeError("Operand must be a number")

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        if isinstance(scalar, (int, float)):
            return Vector2(self.x / scalar, self.y / scalar)
        raise TypeError("Operand must be a number")

    def __eq__(self, other):
        if isinstance(other, Vector2):
            return self.x == other.x and self.y == other.y
        return False

    def __str__(self):
        return f"({self.x},{self.y})"

    def __repr__(self):
        return f"({self.x},{self.y})"

    def distance_to(self, other):
        """Calculate the Euclidean distance to another vector."""
        if isinstance(other, Vector2):
            return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)
        raise TypeError("Argument must be an instance of Vector2")

    def module(self):
        """Return the magnitude (length) of the vector."""
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        """Return a normalized (unit) vector."""
        mag = self.module()
        if mag == 0:
            return Vector2(0, 0)
        return self / mag

    def dot(self, other):
        """Calculate the dot product with another vector."""
        if isinstance(other, Vector2):
            return self.x * other.x + self.y * other.y
        raise TypeError("Argument must be an instance of Vector2")

    def angle_to(self, other):
        """Calculate the angle in radians to another vector."""
        if isinstance(other, Vector2):
            dot_product = self.dot(other)
            mag_product = self.module() * other.module()
            if mag_product == 0:
                raise ValueError("Cannot calculate angle with zero-length vector")
            return math.acos(dot_product / mag_product)
        raise TypeError("Argument must be an instance of Vector2")
    
    def angle_with_x_axis(self):
        """
        Calculate the angle between a 2D vector and the positive x-axis.

        Parameters:
            vector (tuple): A tuple representing the vector (x, y).

        Returns:
            float: Angle in degrees.
        """
        x, y = self.x, self.y
        angle = math.atan2(y, x)
        return angle if angle >= 0 else angle + math.pi*2
    
    def rotate(self, angle : float):
        """Rotate the angle in radians"""
        x = self.x*math.cos(angle) - self.y*math.sin(angle)
        y = self.x*math.sin(angle) + self.y*math.cos(angle)
        new_v : Vector2 = Vector2(x,y)
        return new_v

    def to_tuple(self):
        """Return a tuple representation of the vector."""
        return (self.x, self.y)

    @staticmethod
    def from_tuple(tup):
        """Create a Vector2 instance from a tuple."""
        if len(tup) != 2:
            raise ValueError("Tuple must have exactly 2 elements")
        return Vector2(tup[0], tup[1])