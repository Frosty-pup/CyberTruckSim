# CyberTruck Simulator

Welcome to **CyberTruck Simulator**, a fun and challenging driving simulation game where you manage a CyberTruck's battery, handle mechanical failures, navigate obstacles, and manage costs while trying to make your way to the destination.

## Features

- **Battery Management**: Keep your CyberTruck charged and plan your stops at charging stations.
- **Mechanical Failures**: Encounter and fix random mechanical issues, with some requiring a visit to the Tesla Service Center.
- **Cost Management**: Handle costs for charging and repairs, including expensive visits to the service center and tow truck fees.
- **Obstacles**: Navigate through various obstacles like roadblocks, traffic jams, bad weather, and wildlife crossings.
- **Tweet Feature**: After delays, you can send humorous tweets to Elon Musk with a touch of positivity: "I still love the truck!"

## Installation

To run the game, you'll need Python installed on your system. The game is compatible with Python 3.6 and above.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/hargikas/CyberTruckSim.git
   ```

2. **Navigate to the project directory**:
   ```bash
   cd CyberTruckSim
   ```

3. **Run the game**:
   ```bash
   python cybertruck_cl.py
   ```

## How to Play

1. **Start the Truck**: Begin your journey by starting the CyberTruck.
2. **Drive**: Move towards your destination while managing the battery and dealing with random failures.
3. **Manage Failures**: Address any issues that arise. Some may require expensive repairs or visits to the service center.
4. **Charge**: Stop at charging stations to recharge the battery and continue your journey.
5. **Handle Obstacles**: Deal with various obstacles that affect your progress.
6. **Check Status**: Monitor your truck's status, including battery level, distance traveled, and finances.
7. **Send Tweets**: After encountering delays, choose to send a tweet to Elon Musk to lighten the mood.

## Game Controls

- 1: Start the truck
- 2: Stop the truck
- 3: Drive
- 4: Fix the truck
- 5: Get Towed - Charge the car
- 6: Check status
- 7: Exit the game

## Example Gameplay

Here's a brief example of what you might encounter in the game:

   ```vbnet
   ______________________________________________
  / _________   _____________   _______________  |
 | |    _   _| |__   ___ _ __| |_ __ _   _  ___| | __
 | |   | | | | '_ \ / _ \ '__| | '__| | | |/ __| |/ /
 | |___| |_| | |_) |  __/ |  | | |  | |_| | (__|   <
  \_____\__, |_.__/ \___|_|  | |_|   \__,_|\___|_|\_\
      _____/ |               | |      _
     /______/                | |     | |
    | (___  _ _ __ ___  _   _| | __ _| |_ ___  _ ___
     \___ \| | '_ ` _ \| | | | |/ _` | __/ _ \| '___|
  _______) | | | | | | | |_| | | (_| | || (_) | |
 |________/|_|_| |_| |_|\__,_|_|\__,_|\__\___/|_|

         ----------------------------------
         | What would you like to do?     |
         |  1. Start the truck            |
         |  2. Stop the truck             |
         |  3. Drive                      |
         |  4. Fix the truck              |
         |  5. Get Towed - Charge the car |
         |  6. Check status               |
         |  7. Exit                       |
         ----------------------------------
   
   Enter the number of your choice: 3
   
   Driving... Traveled 5 miles.
   Oh no! A mechanical failure has occurred. You need to fix it before you can continue.
   Repairing mechanical failure will cost you $100.
   Remaining money: $900
   
   Would you like to send a tweet to Elon Musk about your experience? (yes/no): yes
   Sending tweet: 'Just another day with the CyberTruck, but still pushing through! I still love the truck!'
   ```

## Contributing

Feel free to fork the repository, submit pull requests, and suggest features or improvements. All contributions are welcome!

Due to the nature of Cybertruck, which is made of bright metal with mostly straight edges, any dimensional variation shows up like a sore thumb.

All parts of this simulator, whether code or UI, need to be designed and built to sub 10 micron accuracy.

If LEGO and soda cans, which are very low cost, can do this, so can we.

Precision predicates perfectionism.

## License

Copying and distribution of this file, with or without modification, are permitted in any medium provided you do not contact the author about the file or any problems you are having with the file
