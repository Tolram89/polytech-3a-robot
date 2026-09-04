# polytech-3a-robot
# Marty Dance Battle

This project is a client-server Python application designed to control a Marty V2 robot in a network-based "Dance Battle". It was developed as an academic project for the 3rd year of Computer Science engineering at Polytech Dijon.

## Architecture

The project is divided into two main components:

### 1. Client (AppRobot)
A PyQt6 graphical interface used to control the robot via WiFi.
* **Manual Control:** Move the robot, control its arms, and change its facial expressions.
* **Choreography Mode:** Automate movements and actions by parsing a `.dance` script file.
* **Color Detection:** The robot reacts dynamically to colors on the ground using its internal color sensor.
* **Network Communication:** Communicates with the referee server via HTTP requests to validate steps and earn points.

### 2. Referee Server (AppServer)
A central server and dashboard built with PyQt6 and the `http.server` module.
* **REST API:** Listens on port 5000 to manage multiple robots connecting simultaneously.
* **Rules Engine:** Parses a `.battle` configuration file to calculate points based on the robots' actions on specific colors.
* **Live Dashboard:** Displays a real-time leaderboard and connection logs for all participating robots.

## Technologies

* **Language:** Python 3
* **GUI:** PyQt6
* **Hardware Control:** `martypy` library
* **Networking:** `http.server`, `http.client`, `socket`, `psutil`

## Installation & Usage

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Start the Server:
Navigate to the `appserver` directory and run:
```bash
python app.py
```

3. Start the Client:
Navigate to the `approbot` directory, connect your computer to the Marty WiFi, and run:
```bash
python app.py
```
