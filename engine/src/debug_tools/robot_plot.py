import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sysmic_kit import RobotData
class RobotPlot:
    def __init__(self,interval=100):
        """
        Initializes the real-time plotting environment for the robot.

        Parameters:
        - xlim: tuple (min, max) for the x-axis limits
        - ylim: tuple (min, max) for the y-axis limits
        - interval: int, update interval in milliseconds
        """
        self.robot_position = [0, 0]  # Initial position (x, y)
        self.speed = 0
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim((-4.5, 4.5))
        self.ax.set_ylim((-3, 3))
        self.robot_dot, = self.ax.plot([], [], 'bo', markersize=8)
        # Text annotation for speed
        self.speed_text = self.ax.text(0.05, 0.95, '', transform=self.ax.transAxes, ha='left', va='top')
        
        self.ani = FuncAnimation(self.fig, self._update, blit=True, interval=interval)

    def _update(self, frame):
        # Update the robot's position on the plot
        self.robot_dot.set_data(self.robot_position[0], self.robot_position[1])
        self.speed_text.set_text(f'Speed: {self.speed:.2f} m/s')
        return self.robot_dot, self.speed_text

    def update_plot(self, data : RobotData):
        """
        Updates the plot in real-time. Use this in the main loop with plt.pause()
        to prevent blocking.
        """
        self.robot_position = data.position.x, data.position.y
        self.speed = data.velocity.module()
        plt.pause(0.0016)  # Pause to allow the plot to refresh
