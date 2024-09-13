# Licenses: Copying and distribution of this file, with or without modification, are permitted in any medium
# provided you do not contact the author about the file or any problems you are having with the file.

import random
import time
from bisect import bisect_left
import os
import time

def printslow(text):
    for x in text:
        print(x, end="", flush=True)
        time.sleep(0.05)
 

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
        self.happiness = 100
        self.distance = 0
        self.is_running = False
        self.battery_level = 100  # Battery starts at 100%
        self.issues = ["mechanical failure", "crash", "stuck in mud",
                       "tire puncture", "broken GigaWiper", "shattered windshield", "flying panel",
                       "leaking tonneau", "whompy wheel", "snapped frame", "dead battery", "red screen of death"]
        self.fail_chance = 0.3  # 30% chance of random failure
        self.total_distance = 1000  # Distance to the destination
        self.failure_occurred = False
        self.charging_stations = self.generate_charging_stations()
        self.battery_depletion_rate = 100.0/320.0  # Default battery depletion rate
        self.obstacles = ["MAGA rally", "traffic jam",
                          "bad weather", "raccoon attack"]
        self.obstacle_chance = 0.3  # 30% chance of encountering an obstacle
        self.money = 10000  # Start with $10000
        self.repair_costs = {
            "mechanical failure": 1000,
            "crash": 1500,
            "stuck in mud": 100,
            "tire puncture": 50,
            "broken GigaWiper": 150,
            "shattered windshield": 1500,
            "flying panel": 200,
            "leaking tonneau": 250,
            "whompy wheel": 300,
            "snapped frame": 1500,
            "dead battery": 0,  # No cost, just requires charging
            "red screen of death": 0,  # No cost, just ends the game
        }
        self.tow_truck_cost = 200  # Tow truck cost
        self.service_center_cost = 1000  # Tesla Service Center cost
        self.failure_issue = None

    def generate_charging_stations(self):
        # Generate random charging stations between 10 and 90 miles
        offset = 10
        no_stations = 30
        stations = random.sample(range(offset, self.total_distance - offset), no_stations)
        stations.sort()
        return stations

    def start_truck(self):
        if not self.is_running and not self.failure_occurred:
            print("\nStarting the CyberTruck... Vroom Vroom!\n")
            self.is_running = True
        elif self.failure_occurred:
            print("\nYou can't start the truck until the issue is fixed.\n")
        else:
            print("\nThe CyberTruck is already running.\n")

    def stop_truck(self):
        if self.is_running:
            print("\nStopping the CyberTruck...\n")
            self.is_running = False
        else:
            print("\nThe CyberTruck is already stopped.\n")

    def drive(self):
        if self.is_running and not self.failure_occurred:
            if self.battery_level > 0:
                distance_this_drive = random.randint(1, 50)  # Drive between 1 and 50 miles
                print(f"\nDriving... Traveled {distance_this_drive} miles.\n")
                self.distance += distance_this_drive
                self.battery_level -= int(round(distance_this_drive * self.battery_depletion_rate, 0))

                # Check for charging station
                if self.distance in self.charging_stations:
                    print(f"\nYou've reached a charging station at mile {self.distance}.")
                    self.charge_battery()

                # Check for random failures
                if random.random() < self.fail_chance:
                    self.failure_occurred = True
                    self.trigger_failure()
                # Else if no failure, check for obstacles
                elif random.random() < self.obstacle_chance:
                    self.trigger_obstacle()

                # Check if the player reached the destination
                if self.distance >= self.total_distance:
                    print("\nCongratulations! You've reached your destination!")
                    self.stop_truck()
                    print(f"\nYou have spent ${10000 - self.money} to travel {self.total_distance} miles.")
                    return True

                # Check if battery is too low
                if self.battery_level <= 0:
                    print("\nOH NO!\n   Your battery is empty.\n   Recharge quickly before your truck bricks!")
                    self.trigger_failure("dead battery")
            else:
                print("\nOH NO!!\n   Your battery is empty.\n   Recharge quickly before your truck bricks!")
                self.trigger_failure("dead battery")
        else:
            print("\nYOU CAN'T DRIVE!\n   The truck is either stopped or has an issue.\n")

        # Reset depletation rate (in case an event has happened)
        self.battery_depletion_rate = 100.0/320.0
        return False

    def trigger_failure(self, issue=None):
        if not issue:
            issue = random.choice(self.issues)
        if issue == "red screen of death":
            print(f"OH NO!\n   The dreaded {issue} has occurred.\n"
                  f"   Your CyberTruck just bricked itself and caught fire.\n")
            self.splash_game_over()
            exit()
        print(f"OH NO!\n   A {issue} has occurred.\n   You need to fix it before you can continue.\n")
        self.is_running = False
        self.failure_issue = issue

    def pay_for_repair(self, issue):
        repair_cost = self.repair_costs.get(issue, 0)

        # 30% chance you need a tow truck
        if random.random() < 0.3 and issue != "dead battery":
            print("You need a flatbed tow truck for this repair!")
            repair_cost += self.tow_truck_cost

        # 20% chance for Tesla Service Center for major issues
        if issue in ["mechanical failure", "crash", "flying panel", "snapped frame",
                     "broken GigaWiper", "whompy wheel", "shattered windshield"] and random.random() < 0.2:
            print("\nThis issue requires a visit to the Tesla Service Center!")
            self.visit_service_center()

        if self.money >= repair_cost:
            print(f"\nRepairing {issue} costed ${repair_cost}.")
            self.money -= repair_cost
            print(f"Money left: ${self.money}")
            # happiness decreases as failures occur
            # self.modify_happiness(-120) # TO TEST EASILY
            self.modify_happiness(-random.randint(5, 15))
        else:
            print(f"\nYou don't have enough money (${self.money}) to repair the {issue}.\n")
            self.splash_game_over()
            exit()

        self.failure_occurred = False

    def visit_service_center(self):
        print("\nVISITING TESLA SERVICE CENTER...\n   This will be very expensive and time-consuming!")
        service_center_time = random.randint(
            5, 10)  # Simulate a long delay in days
        # Simulate the time passing (shortened for playability)
        i = 0
        while i < service_center_time:
            time.sleep(1)
            print(f"   ...")
            i += 1
        print(f"   Spent {service_center_time} days looking into it at the service center.")

        # Thanks to JeanLuc_Moultonde: https://shorturl.at/o2Ox3
        if random.random() < 0.1:
            print("\n\nTruck is totaled, sorry we can't do shit.\n")
            self.splash_game_over()
            exit()

        if self.money >= self.service_center_cost:
            print(f"\nService center visit costed ${self.service_center_cost}.")
            self.money -= self.service_center_cost
            print(f"Money left: ${self.money}")
        else:
            print(f"\nYou don't have enough money (${self.money}) to pay for the Tesla Service Center.\n")
            print(f"\nBUT WE HAVE AN IDEA...")
            self.prompt_for_resale()

    def fix_issue(self):
        if self.failure_occurred:
            if "dead battery" in self.issues and self.battery_level <= 0:
                print("\nYou can't fix the issue without charging first.")
            else:
                self.pay_for_repair(self.failure_issue)
                self.prompt_for_tweet()
                self.failure_occurred = False
                self.failure_issue = None
        else:
            print("\nThere's nothing to fix right now.\n")

    def charge_battery(self):
        # $5 per percentage of battery charged
        charge_cost = (100 - self.battery_level) * 5
        if self.money >= charge_cost:
            print(f"Charging the CyberTruck will cost you ${charge_cost}.")
            # Simulate charging time
            i = 0
            while i < 5:
                time.sleep(1)
                print(f"...")
                i += 1
            self.battery_level = 100
            self.money -= charge_cost
            print(f"The battery is now fully charged.\nRemaining money: ${self.money}\n")
        else:
            print(f"\nYou don't have enough money (${self.money}) to charge the battery.\n")
            self.splash_game_over()
            exit()

    def tow_and_charge_battery(self):
        print("You need a flatbed tow truck to get you to the nearest charging station!")
        self.money -= self.tow_truck_cost
        self.distance = take_closest(self.charging_stations, self.distance)
        self.charge_battery()
        if self.failure_issue == "dead battery":
            self.failure_occurred = False
            self.failure_issue = None

    def check_status(self):
        print(f"\nCURRENT STATUS:\n- Distance traveled: {self.distance} miles\n- Battery level: {self.battery_level}%\n"
              f"- Money: ${self.money}\n- Your happiness: {self.happiness}%\n- Truck running: {self.is_running}\n")
        if self.failure_occurred:
            print("Warning: The truck has an issue that needs to be fixed!\n")
        print(f"Charging stations ahead at: {', '.join(map(str, self.charging_stations))} miles\n")

    def trigger_obstacle(self):
        obstacle = random.choice(self.obstacles)
        print(f"{obstacle.upper()}")

        if obstacle == "MAGA rally":
            print(f"   A MAGA rally of {random.randint(1, 12)} people is blocking the road.\n   "
                  "You make a detour, delaying your journey.\n")
            # Set back distance by a few miles (as a detour)
            self.distance -= random.randint(1, 50)
        elif obstacle == "traffic jam":
            print("   You're stuck in a traffic jam!\n   Progress is slower for the next few miles.\n")
            self.battery_depletion_rate *= 3  # Increase battery depletion for the next period
        elif obstacle == "bad weather":
            print("   Bad weather is making it harder to drive.\n   Battery depletes faster, tonneau starts to leak.\n")
            self.battery_depletion_rate *= 4  # Battery depletes faster due to weather
        elif obstacle == "raccoon attack":
            print("   Racoons are trying to break in the tonneau while you're at the red light.\n"
                  "   Drive before they eat the plastic bed!\n")
            time.sleep(2)  # Simulate a short wait while at the red light

    def modify_happiness(self, value):
        self.happiness += value
        # if happiness is below zero, User is offered to sell his shitty truck
        if self.happiness <= 0:
            print("\nYOUR SATISFACTION IS VERY LOW...")
            self.prompt_for_resale()

    def prompt_for_resale(self):
        ads = [
            f"CyberBeast for sale! Best truck I've ever driven. Too bad I'm moving to the UK. Don't sleep!",
            f"My garage is too small, I'm sad I have to sell my lovely Beast. Don't miss your chance!",
            f"Wife will divorce and leave with her boyfriend if I decide to keep my truck. That's why I'm selling.",
            f"Selling my CyberTruck, only to upgrade to a CyberBeast ;)",
            f"Proud texan moving to NYC, very sad I can't bring my CyberTruck with me.",
        ]
        user_choice = input("\nWe give you the opportunity to list "
                            "an ad to get rid of your WankPanzer.\nAre you in? (yes/no): ").lower()
        if user_choice == 'yes' or user_choice == 'y':
            ad = random.choice(ads)
            print(f"\nListing an ad:\n   '{ad}\n   Only {self.distance} miles!'")
            time.sleep(3)  # Simulate the wait for a buyer
            if random.random() < 0.4:
                print("\n=======================================================")
                print("CONGRATULATIONS!\nSomeone bought your CyberTruck "
                      "before it bricked itself!\nYou're now free!")
                print("========================================================\n")
            else:
                print("WE HAVE BAD NEWS FOR YOU...")
                print("   Two weeks have passed, and nobody wanted to buy your CyberTruck...\n")
                self.splash_game_over()
            exit()
        else:
            print("You had the opportunity to sale your shitbox, but you decided to keep it?\n"
                  "That's some serious Stockholm Syndrome we got here!\nStill love the truck, hey?\n")
            self.splash_game_over()
            exit()

    def prompt_for_tweet(self):
        if self.happiness >= 66:
            tweets = [
                "Just another day with the CyberTruck, but still pushing through!\n",
                "Having some trouble with the CyberTruck, but it's all part of the adventure!\n",
                "Another delay, but I trust the CyberTruck will get me through!\n",
                "Faced a few bumps on the road today with my CyberTruck.\n",
                "The CyberTruck and I are taking a small break due to issues, but we'll be back on the road soon!\n",
            ]
            magic_sentences = [
                "Still love the truck though!\n   @elon #cyberbeast #vroooom",
                "Best truck ever though!\n   @elon #teslacybertruck #truckstuff",
                "Still love my CT, thanks Elon!\n   @elon @tesla #cybertruck",
            ]
        elif 66 > self.happiness >= 33:
            tweets = [
                "Elon, please fix this thing ASAP, it drives me crazy!\n",
                "Build quality and performance are far below my expectations, hope next update will improve it!\n",
                "I traded in my reliable sedan for this piece of engineering art that can't even keep the rain out!\n",
                "I'm so glad I spent my hard-earned cash on a vehicle that's more prone to dents than a tin can.\n",
                "Not exactly the kind of adventure I was hoping for!\n",
            ]
            magic_sentences = [
                "Still love the truck though!\n   @elon @ #truckstuff #teslacybertruck",
                "Elon, please help!\n   @elon @tesla #cyberbeast #vroooom  #truckstuff",
                "Still love the Beast tho!\n   @elon @tesla #cybertruck",
            ]
        elif self.happiness < 33:
            tweets = [
                "Really disappointed with the build quality issues I've encountered!\n",
                "Worst car ever. Elon, you should definitely look into it!\n",
                "One more problem and I'll sell that shiny turd!\n",
                "My Cybertruck's bulletproof windows shatter at the slightest touch—truly a feature, not a flaw!\n",
                "Another update that turns my Cybertruck into a glorified paperweight.\n",
            ]
            magic_sentences = [
                "Worst truck ever! A pure lemon!\n   @elon @tesla #elonsux #cybersuck",
                "I hate you Elon, fck Tesla!\n   @elon @tesla #fckcyberbeast #felon",
                "Hate that shitbox!\n   @elon @tuckfesla #disappointedtrucker",
            ]

        user_choice = input("\nWould you like to send a tweet to Elon Musk about your experience? (yes/no): ").lower()

        if user_choice == 'yes' or user_choice == 'y':
            os.system('cls' if os.name == 'nt' else 'clear')
            # Face image generated from https://adelfaure.itch.io/ascii-facemaker, license allows free use - 
            print("        ______________________  ")
            print("        |       .-~~~-.      |        Welcome to ") 
            print("        |      /       \     |      ____/\__.__    .__  __    __                 ")     
            print("        |      !       !     |     /   / /_/|  |__ |__|/  |__/  |_  ___________  ")    
            print("        |     (~[=]-[=]~)    |     \__/ / \ |  |  \|  \   __\   __\/ __ \_  __ \                  ")    
            print("        |      !   L   !     |     / / /   \|   Y  \  ||  |  |  | \  ___/|  | \/             ")      
            print("        |       \  -  /      |    /_/ /__  /|___|  /__||__|  |__|  \___  >__|             ")      
            print("        |       !`._.'!      |      \/   \/      \/                    \/            ")       
            print("        |      /       \     |              ")      
            print("        | _.-~'         `~-._|          The cybertrucks own social media platform      ") 
            print("        |'                   |                 ") 
            print("        ----------------------                 ") 
            

            tweet = random.choice(tweets) + "   " + random.choice(magic_sentences)
            print("\nWhat's on your mind, cashcow?:\n")
            printslow(f"   '{tweet}'\n")
        else:
            print("\nNO TWEET SENT.\n   Warranty voided!\n")

    def splash_game_over(self):
        print(" =============================== ")
        print("|                               |")
        print("|       G A M E    O V E R      |")
        print("|                               |")
        print(" =============================== \n")

def game_loop():
    truck_sim = CyberTruckSimulator()
    game_over = False

    print("\n======================================================")
    print("        Welcome to the CyberTruck Simulator!")
    print("======================================================")
    print("   ______________________________________________     ")
    print("  / _________   _____________   _______________  |    ")
    print(" | |    _   _| |__   ___ _ __| |_ __ _   _  ___| | __ ")
    print(" | |   | | | | '_ \\ / _ \\ '__| | '__| | | |/ __| |/ / ")
    print(" | |___| |_| | |_) |  __/ |  | | |  | |_| | (__|   <  ")
    print("  \\_____\\__, |_.__/ \\___|_|  | |_|   \\__,_|\\___|_|\\_\\ ")
    print("      _____/ |               | |      _                  ")
    print("     /______/                | |     | |                 ")
    print("    | (___  _ _ __ ___  _   _| | __ _| |_ ___  _ ___ ")
    print("     \\___ \\| | '_ ` _ \\| | | | |/ _` | __/ _ \\| '___|")
    print("  _______) | | | | | | | |_| | | (_| | || (_) | |        ")
    print(" |________/|_|_| |_| |_|\\__,_|_|\\__,_|\\__\\___/|_|        \n")

    while not game_over:
        print("         ----------------------------------")
        print("         | What would you like to do?     |")
        print("         |  1. Start the truck            |")
        print("         |  2. Stop the truck             |")
        print("         |  3. Drive                      |")
        print("         |  4. Fix the truck              |")
        print("         |  5. Get Towed - Charge the car |")
        print("         |  6. Check status               |")
        print("         |  7. Exit                       |")
        print("         ----------------------------------")

        choice = input("\nEnter the number of your choice: ")

        if choice == '1':
            os.system('cls' if os.name == 'nt' else 'clear')
            truck_sim.start_truck()
        elif choice == '2':
            os.system('cls' if os.name == 'nt' else 'clear')
            truck_sim.stop_truck()
        elif choice == '3':
            os.system('cls' if os.name == 'nt' else 'clear')
            game_over = truck_sim.drive()
        elif choice == '4':
            os.system('cls' if os.name == 'nt' else 'clear')
            truck_sim.fix_issue()
        elif choice == '5':
            os.system('cls' if os.name == 'nt' else 'clear')
            truck_sim.tow_and_charge_battery()
        elif choice == '6':
            os.system('cls' if os.name == 'nt' else 'clear')
            truck_sim.check_status()
        elif choice == '7':
            print("Exiting the simulator. Goodbye!\n")
            break
        else:
            print("Invalid input. Please choose a valid option.\n")


# Run the game loop
if __name__ == "__main__":

    game_loop()
