import pygame
from world.world import World
from sysmic_kit.entities import *
from sysmic_kit.geometry import *
# Constants
FIELD_WIDTH = 900  # in cm (9m)
FIELD_HEIGHT = 600  # in cm (6m)
MARGIN = 50  # Additional margin around the field in pixels
WINDOW_WIDTH = FIELD_WIDTH + 2 * MARGIN
WINDOW_HEIGHT = FIELD_HEIGHT + 2 * MARGIN
LINE_WIDTH = 2

# Colors
BACKGROUND = (165,172,175)
WHITE = (0,20,51)
RED = (51,20,51)
BLACK = (0, 0, 0)

class UI:
    def __init__(self, world: World):
        # Initialize pygame
        pygame.init()
        # Initialize the display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("RoboCup SSL Field")
        self.running = True
        self.clock = pygame.time.Clock()
        self.world = world
        self.robot_trace = []
        self.font = pygame.font.Font(None, 36)  # Default pygame font, size 36

    # Convert field coordinates to screen coordinates
    def field_to_screen(self, x, y):
        screen_x = WINDOW_WIDTH/2 + (x*WINDOW_WIDTH)/9
        screen_y = WINDOW_HEIGHT/2 - (y*WINDOW_HEIGHT)/6
        return screen_x, screen_y
    
    # Display the robot's position
    def display_velocity(self, x, y):
        text = f"Velocity:({x:.3f}, {y:.3f}), {abs(x+y):.3f}"
        text_surface = self.font.render(text, True, WHITE)
        self.screen.blit(text_surface, (10, 10))  # Top-left corner of the screen
    
    # Draw the field
    def draw_field(self):
        # Fill background
        self.screen.fill(BACKGROUND)

        # Field boundaries
        pygame.draw.rect(
            self.screen,
            WHITE,
            (MARGIN, MARGIN, FIELD_WIDTH, FIELD_HEIGHT),
            LINE_WIDTH,
        )


    # Draw a robot
    def draw_robot(self, x, y, orientation, color):
        robot_radius = 15  # Arbitrary radius in pixels
        screen_x, screen_y = self.field_to_screen(x, y)
        pygame.draw.circle(self.screen, color, (screen_x, screen_y), robot_radius)
        
        init_line = (screen_x, screen_y)
        
        final_line = (screen_x + robot_radius*math.cos(-orientation) , screen_y + robot_radius*math.sin(-orientation))
        pygame.draw.line(self.screen, BACKGROUND, init_line, final_line, width=2)
        # Add the robot's position to the trace
        self.robot_trace.append((x, y))

        # Limit the trace length to avoid excessive memory usage (e.g., last 100 points)
        #if len(self.robot_trace) > 100:
        #    self.robot_trace.pop(0)
        self.draw_trace(self.robot_trace)
            
    def draw_trace(self,trace):
        for i in range(1, len(trace)):
            start = self.field_to_screen(trace[i - 1][0], trace[i - 1][1])
            end = self.field_to_screen(trace[i][0], trace[i][1])
            pygame.draw.line(self.screen, WHITE, start, end, 2)  # Line width = 2
        
    # Main loop
    def loop(self) -> bool:
        if self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False


            self.draw_field()

            for r in self.world.get_robots_blue():
                self.draw_robot(r.position.x, r.position.y, r.orientation,WHITE)  # Robot to the top-right
                self.display_velocity(r.velocity.x, r.velocity.y )
            

            # Update the display
            pygame.display.flip()
            self.clock.tick(200)
            return True
        else:
            pygame.quit()
            return False
