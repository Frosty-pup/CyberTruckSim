import pygame
import random
import time

# Initialize pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CyberTruck Simulator")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Load font
FONT = pygame.font.Font(None, 36)
FONT_SMALL = pygame.font.Font(None, 24)

# Define a simple button class
class Button:
    def __init__(self, text, x, y, width, height, color, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.action = action
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text = FONT.render(self.text, True, WHITE)
        screen.blit(text, (self.x + (self.width - text.get_width()) // 2, self.y + (self.height - text.get_height()) // 2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Define the CyberTruck simulation class
class CyberTruckSimulator:
    def __init__(self):
        self.distance = 0
        self.is_running = False
        self.battery_level = 100  # Battery starts at 100%
        self.issues = ["mechanical failure", "crash", "stuck in mud", "tire puncture", "battery dead"]
        self.fail_chance = 0.2  # 20% chance of random failure
        self.total_distance = 100  # Distance to the destination
        self.failure_occurred = False
        self.charging_stations = self.generate_charging_stations()
        self.battery_depletion_rate = 5  # Default battery depletion rate
        self.money = 1000  # Start with $1000
        self.repair_costs = {
            "mechanical failure": 100,
            "crash": 150,
            "stuck in mud": 50,
            "tire puncture": 30,
            "battery dead": 0,  # No cost, just requires charging
        }
        self.tow_truck_cost = 200  # Tow truck cost
        self.service_center_cost = 500  # Tesla Service Center cost
        self.status_message = "Welcome to CyberTruck Simulator!"
    
    def generate_charging_stations(self):
        stations = random.sample(range(10, 90), 3)
        stations.sort()
        return stations

    def start_truck(self):
        if not self.is_running and not self.failure_occurred:
            self.is_running = True
            self.status_message = "CyberTruck is now running."
        elif self.failure_occurred:
            self.status_message = "Fix the issue before starting the truck."
        else:
            self.status_message = "CyberTruck is already running."

    def stop_truck(self):
        if self.is_running:
            self.is_running = False
            self.status_message = "CyberTruck is now stopped."
        else:
            self.status_message = "CyberTruck is already stopped."

    def drive(self):
        if self.is_running and not self.failure_occurred:
            if self.battery_level > 0:
                distance_this_drive = random.randint(1, 10)
                self.distance += distance_this_drive
                self.battery_level -= self.battery_depletion_rate
                self.status_message = f"Driving... You traveled {distance_this_drive} miles. Distance: {self.distance} miles."

                # Check for charging station
                if self.distance in self.charging_stations:
                    self.charge_battery()

                # Check for random failures
                if random.random() < self.fail_chance:
                    self.failure_occurred = True
                    self.trigger_failure()

                # Check if battery is too low
                if self.battery_level <= 0:
                    self.trigger_failure("battery dead")

                # Check if destination reached
                if self.distance >= self.total_distance:
                    self.status_message = "Congratulations! You've reached the destination!"
                    self.is_running = False
            else:
                self.trigger_failure("battery dead")
        else:
            self.status_message = "Can't drive! Either the truck is stopped or an issue occurred."

    def charge_battery(self):
        charge_cost = (100 - self.battery_level) * 2  # $2 per percentage of battery charged
        if self.money >= charge_cost:
            self.battery_level = 100
            self.money -= charge_cost
            self.status_message = f"Charging complete. Charged for ${charge_cost}. Remaining money: ${self.money}"
        else:
            self.status_message = "Not enough money to charge!"

    def trigger_failure(self, issue=None):
        if not issue:
            issue = random.choice(self.issues)
        repair_cost = self.repair_costs.get(issue, 0)
        self.money -= repair_cost
        self.status_message = f"Failure: {issue}. Repair cost: ${repair_cost}. Remaining money: ${self.money}"
        self.is_running = False
        self.failure_occurred = True

    def fix_issue(self):
        if self.failure_occurred:
            self.status_message = "Issue fixed! You can drive again."
            self.failure_occurred = False
        else:
            self.status_message = "No issues to fix!"

    def check_status(self):
        return f"Distance: {self.distance} miles, Battery: {self.battery_level}%, Money: ${self.money}, Truck running: {self.is_running}"

# Initialize the game objects
sim = CyberTruckSimulator()

# Set up buttons
start_button = Button("Start Truck", 50, 450, 150, 50, GREEN, sim.start_truck)
stop_button = Button("Stop Truck", 220, 450, 150, 50, RED, sim.stop_truck)
drive_button = Button("Drive", 390, 450, 150, 50, BLUE, sim.drive)
fix_button = Button("Fix Issue", 560, 450, 150, 50, BLACK, sim.fix_issue)

# Main game loop
running = True
while running:
    screen.fill(WHITE)
    
    # Draw UI elements
    status_text = FONT_SMALL.render(sim.status_message, True, BLACK)
    screen.blit(status_text, (50, 50))

    truck_status = sim.check_status()
    truck_status_text = FONT_SMALL.render(truck_status, True, BLACK)
    screen.blit(truck_status_text, (50, 100))

    # Draw buttons
    start_button.draw(screen)
    stop_button.draw(screen)
    drive_button.draw(screen)
    fix_button.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if start_button.is_clicked(mouse_pos):
                start_button.action()
            elif stop_button.is_clicked(mouse_pos):
                stop_button.action()
            elif drive_button.is_clicked(mouse_pos):
                drive_button.action()
            elif fix_button.is_clicked(mouse_pos):
                fix_button.action()

    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
