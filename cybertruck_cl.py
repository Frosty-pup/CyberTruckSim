# Licenses: Copying and distribution of this file, with or without modification, are permitted in any medium provided you do not contact the author about the file or any problems you are having with the file.

import random
import time
from bisect import bisect_left


def take_closest(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
        return after
    else:
        return before


class CyberTruckSimulator:
    def __init__(self):
        self.distance = 0
        self.is_running = False
        self.battery_level = 100  # Battery starts at 100%
        self.issues = ["mechanical failure", "crash",
                       "stuck in mud", "tire puncture", "battery dead"]
        self.fail_chance = 0.3  # 30% chance of random failure
        self.total_distance = 1000  # Distance to the destination
        self.failure_occurred = False
        self.charging_stations = self.generate_charging_stations()
        self.battery_depletion_rate = 100.0/320.0  # Default battery depletion rate
        self.obstacles = ["roadblock", "traffic jam",
                          "bad weather", "wildlife crossing"]
        self.obstacle_chance = 0.3  # 30% chance of encountering an obstacle
        self.money = 10000  # Start with $10000
        self.repair_costs = {
            "mechanical failure": 1000,
            "crash": 1500,
            "stuck in mud": 100,
            "tire puncture": 50,
            "battery dead": 0,  # No cost, just requires charging
        }
        self.tow_truck_cost = 200  # Tow truck cost
        self.service_center_cost = 1000  # Tesla Service Center cost
        self.failure_issue = None

    def generate_charging_stations(self):
        # Generate random charging stations between 10 and 90 miles
        offset = 10
        no_stations = 30
        stations = random.sample(
            range(offset, self.total_distance - offset), no_stations)
        stations.sort()
        return stations

    def start_truck(self):
        if not self.is_running and not self.failure_occurred:
            print("\nStarting the CyberTruck... Vroom Vroom!")
            self.is_running = True
        elif self.failure_occurred:
            print("You can't start the truck until the issue is fixed.")
        else:
            print("The CyberTruck is already running.")

    def stop_truck(self):
        if self.is_running:
            print("\nStopping the CyberTruck...")
            self.is_running = False
        else:
            print("The CyberTruck is already stopped.")

    def drive(self):
        if self.is_running and not self.failure_occurred:
            if self.battery_level > 0:
                distance_this_drive = random.randint(
                    1, 50)  # Drive between 1 and 50 miles
                print(f"\nDriving... Traveled {distance_this_drive} miles.")
                self.distance += distance_this_drive
                self.battery_level -= int(round(distance_this_drive *
                                          self.battery_depletion_rate, 0))

                # Check for charging station
                if self.distance in self.charging_stations:
                    print(f"\nYou've reached a charging station at mile {
                          self.distance}.")
                    self.charge_battery()

                # Check for random failures
                if random.random() < self.fail_chance:
                    self.failure_occurred = True
                    self.trigger_failure()

                # Check for obstacles
                if random.random() < self.obstacle_chance:
                    self.trigger_obstacle()

                # Check if the player reached the destination
                if self.distance >= self.total_distance:
                    print("\nCongratulations! You've reached your destination!")
                    self.stop_truck()
                    print(f"\n You have spent ${
                          10000 - self.money} to travel {self.total_distance} miles.")
                    return True

                # Check if battery is too low
                if self.battery_level <= 0:
                    print("\nOh no! Your battery is dead. You need to recharge.")
                    self.trigger_failure("battery dead")
            else:
                print("\nThe battery is empty! You need to recharge.")
                self.trigger_failure("battery dead")
        else:
            print("\nYou can't drive! The truck is either stopped or has an issue.")

        # Reset depletation rate (in case an event has happened)
        self.battery_depletion_rate = 100.0/320.0
        return False

    def trigger_failure(self, issue=None):
        if not issue:
            issue = random.choice(self.issues)
        print(f"\nOh no! A {
              issue} has occurred. You need to fix it before you can continue.")
        self.is_running = False
        self.failure_issue = issue

    def pay_for_repair(self, issue):
        repair_cost = self.repair_costs.get(issue, 0)

        # 30% chance you need a tow truck
        if random.random() < 0.3 and issue != "battery dead":
            print("\nYou need a tow truck for this repair!")
            repair_cost += self.tow_truck_cost

        # 20% chance for Tesla Service Center for major issues
        if issue in ["mechanical failure", "crash"] and random.random() < 0.2:
            print("\nThis issue requires a visit to the Tesla Service Center!")
            self.visit_service_center()

        if self.money >= repair_cost:
            print(f"\nRepairing {issue} will cost you ${repair_cost}.")
            self.money -= repair_cost
            print(f"Remaining money: ${self.money}")
        else:
            print(f"\nYou don't have enough money (${
                  self.money}) to repair the {issue}. Game over!")
            exit()

        self.failure_occurred = False

    def visit_service_center(self):
        print("\nVisiting Tesla Service Center... This will be very expensive and time-consuming!")
        service_center_time = random.randint(
            5, 10)  # Simulate a long delay in days
        # Simulate the time passing (shortened for playability)
        time.sleep(service_center_time)
        print(f"Spent {service_center_time} days at the service center.")

        # Thanks to JeanLuc_Moultonde: https://shorturl.at/o2Ox3
        if random.random() < 0.1:
            print("Truck is totaled, sorry we can't do shit. Game over!")
            exit()

        if self.money >= self.service_center_cost:
            print(f"\nService center visit will cost ${
                  self.service_center_cost}.")
            self.money -= self.service_center_cost
            print(f"Remaining money: ${self.money}")
        else:
            print(f"\nYou don't have enough money (${
                  self.money}) to pay for the Tesla Service Center. Game over!")
            exit()

    def fix_issue(self):
        if self.failure_occurred:
            if "battery dead" in self.issues and self.battery_level <= 0:
                print("\nYou can't fix the issue without charging first.")
            else:
                self.pay_for_repair(self.failure_issue)
                self.prompt_for_tweet()
                self.failure_occurred = False
                self.failure_issue = None
        else:
            print("\nThere's nothing to fix right now.")

    def charge_battery(self):
        # $5 per percentage of battery charged
        charge_cost = (100 - self.battery_level) * 5
        if self.money >= charge_cost:
            print(f"\nCharging the CyberTruck will cost you ${charge_cost}.")
            time.sleep(3)  # Simulate charging time
            self.battery_level = 100
            self.money -= charge_cost
            print(f"The battery is now fully charged. Remaining money: ${
                  self.money}")
        else:
            print(f"\nYou don't have enough money (${
                  self.money}) to charge the battery. Game over!")
            exit()

    def tow_and_charge_battery(self):
        print("\nYou need a tow truck to get you to the nearest charging station!")
        self.money -= self.tow_truck_cost
        self.distance = take_closest(self.charging_stations, self.distance)
        self.charge_battery()
        if self.failure_issue == "battery dead":
            self.failure_occurred = False
            self.failure_issue = None

    def check_status(self):
        print(f"\nCurrent status: Distance traveled: {self.distance} miles, Battery level: {
              self.battery_level}%, Money: ${self.money}, Truck running: {self.is_running}")
        if self.failure_occurred:
            print("Warning: The truck has an issue that needs to be fixed!")
        print(f"Charging stations ahead at: {
              ', '.join(map(str, self.charging_stations))} miles")

    def trigger_obstacle(self):
        obstacle = random.choice(self.obstacles)
        print(f"\nObstacle encountered: {obstacle}!")

        if obstacle == "roadblock":
            print("You must stop and wait for a detour. This delays your journey.")
            # Set back distance by a few miles (as a detour)
            self.distance -= random.randint(1, 50)
        elif obstacle == "traffic jam":
            print(
                "You're stuck in a traffic jam! Progress is slower for the next few miles.")
            self.battery_depletion_rate *= 3  # Increase battery depletion for the next period
        elif obstacle == "bad weather":
            print("Bad weather is making it harder to drive. Battery depletes faster.")
            self.battery_depletion_rate *= 4  # Battery depletes faster due to weather
        elif obstacle == "wildlife crossing":
            print("Wildlife is crossing the road. You have to stop and wait.")
            time.sleep(2)  # Simulate a short wait while animals cross the road

    def prompt_for_tweet(self):
        tweets = [
            "Just another day with the CyberTruck, but still pushing through! ",
            "Having some trouble with the CyberTruck, but it's all part of the adventure! ",
            "Another delay, but I trust the CyberTruck will get me through! ",
            "Faced a few bumps on the road today with my CyberTruck. ",
            "The CyberTruck and I are taking a small break due to issues, but we'll be back on the road soon! "
        ]
        user_choice = input(
            "\nWould you like to send a tweet to Elon Musk about the delay? (yes/no): ").lower()

        if user_choice == 'yes':
            tweet = random.choice(tweets) + "I still love the truck!"
            print(f"\nSending tweet: '{tweet}'")
        else:
            print("\nNo tweet sent.")


def game_loop():
    truck_sim = CyberTruckSimulator()
    game_over = False

    print("Welcome to the CyberTruck Simulator!")

    while not game_over:
        print("\nWhat would you like to do?")
        print("1. Start the truck")
        print("2. Stop the truck")
        print("3. Drive")
        print("4. Fix the truck")
        print("5. Get Towed - Charge the car")
        print("6. Check status")
        print("7. Exit")

        choice = input("\nEnter the number of your choice: ")

        if choice == '1':
            truck_sim.start_truck()
        elif choice == '2':
            truck_sim.stop_truck()
        elif choice == '3':
            game_over = truck_sim.drive()
        elif choice == '4':
            truck_sim.fix_issue()
        elif choice == '5':
            truck_sim.tow_and_charge_battery()
        elif choice == '6':
            truck_sim.check_status()
        elif choice == '7':
            print("Exiting the simulator. Goodbye!")
            break
        else:
            print("Invalid input. Please choose a valid option.")


# Run the game loop
if __name__ == "__main__":
    game_loop()
