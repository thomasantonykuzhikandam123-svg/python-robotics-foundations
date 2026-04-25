# ============================================================
# PYTHON ROBOTICS FOUNDATIONS
# Week 1 — Intermediate Python + OOP + NumPy
# RMIT Masters in Robotics and Mechatronics — April 2026
# ============================================================

# ============================================================
# ADDED AFTER FIRST PUSH:
# - log_action decorator
# - dunder methods (__str__, __repr__, __eq__, __len__)
# - @property with setter and ValueError on battery
# - NumPy positions (np.array instead of strings)
# - distance_to() method using np.linalg.norm
# - SensorDataLogger attached to each sensor
# - Inheritance hierarchy (Mobilerobot, Cleaningrobot, Armrobot)
# - RobotFleet class with fleet management methods
# - List and dict comprehensions

import numpy as np
from sensor_logger import SensorDataLogger

# SENSOR CLASS — blueprint for a single sensor
class Sensors:
    def __init__(self, sensor_type, sensor_range, sensor_status):
        self.sensor_type = sensor_type      # type of sensor
        self.sensor_range = sensor_range    # range in metres
        self.sensor_status = sensor_status  # active or inactive
        self.logger = SensorDataLogger()    # logs readings over time

    def status_report(self):
        print(f"Sensor Type: {self.sensor_type}")
        print(f"Range: {self.sensor_range}")
        print(f"Status: {self.sensor_status}")

# creating sensor objects
sensor1 = Sensors('ultrasonic', 7.5, 'Active')
sensor2 = Sensors('camera', 10, 'Inactive')
sensor3 = Sensors('lidar', 15, 'Active')

# simulate some sensor readings on sensor1
sensor1.logger.add_reading(3.5)
sensor1.logger.add_reading(7.2)
sensor1.logger.add_reading(1.1)

# DECORATOR — logs which method was called and on which robot

def log_action(func):
    def wrapper(self, *args, **kwargs):
        print(f"Action: {func.__name__} function is called for {self.name}")
        return func(self, *args, **kwargs)
    return wrapper

# ROBOT CLASS — base blueprint for all robots

class Robot:
    robot_count = 0  # class variable — counts total robots created

    def __init__(self, name, battery, position, sensors):
        self.name = name
        self._battery = battery        # private — accessed via @property
        self.position = position       # np.array([x, y]) for maths
        self.sensors = sensors         # list of Sensor objects
        Robot.robot_count += 1

    @log_action
    def active_sensors(self):
        # list comprehension — filters only active sensors
        active = [sensor for sensor in self.sensors if sensor.sensor_status == 'Active']
        print(f"Active sensors on {self.name}:")
        for sensor in active:
            print(f"  - {sensor.sensor_type} | {sensor.sensor_range}m")

    @log_action
    def display_info(self):
        # prints all robot details including sensors
        print(f"Robot: {self.name}")
        print(f"Battery: {self.battery}")
        print(f"Position: {self.position}")
        print("Sensors:")
        for sensor in self.sensors:
            print(f"  - type: {sensor.sensor_type} | range: {sensor.sensor_range} | status: {sensor.sensor_status}")
        print()

    @classmethod
    def from_config(cls, config_dict):
        # alternative constructor — creates robot from a dictionary
        name = config_dict['name']
        battery = config_dict['battery']
        position = config_dict['position']
        sensors = config_dict['sensors']
        return cls(name, battery, position, sensors)

    @staticmethod
    def validate_battery(battery):
        # utility — checks if battery level is valid (0-100)
        if battery >= 0 and battery <= 100:
            return True
        else:
            return False

    def __str__(self):
        # called when print(robot) — human readable
        return f"Robot: {self.name} | Battery: {self.battery} | Sensors: {len(self.sensors)}"

    def __repr__(self):
        # called when repr(robot) — technical format
        return f"Robot('{self.name}', {self.battery})"

    def __eq__(self, other):
        # two robots are equal if they have the same name
        if isinstance(other, Robot):
            return self.name == other.name
        return NotImplemented

    def __len__(self):
        # len(robot) returns number of sensors
        return len(self.sensors)

    @property
    def battery(self):
        # getter — read battery value
        return self._battery

    @battery.setter
    def battery(self, value):
        # setter — only accepts values between 0 and 100
        if value < 0 or value > 100:
            raise ValueError("Battery level must be between 0 and 100")
        self._battery = value

    def distance_to(self, other_robot):
        # calculates straight line distance to another robot using NumPy
        if isinstance(other_robot, Robot):
            return np.linalg.norm(self.position - other_robot.position)


# CONFIG DICTIONARIES — used with from_config classmethod

config1 = {
    'name': 'picking_robot',
    'battery': 100,
    'position': np.array([2, 3]),
    'sensors': [sensor1, sensor2]
}

config2 = {
    'name': 'assembly_robot',
    'battery': 90,
    'position': np.array([4, 5]),
    'sensors': [sensor2, sensor3]
}

# creating robot objects — robot4 and robot5 via from_config
robot1 = Robot('warehouse_robot', 100, np.array([0, 0]), sensors=[sensor1, sensor2])
robot2 = Robot('robotic_arm', 80, np.array([5, 6]), sensors=[sensor3])
robot3 = Robot('mining_robot', 60, np.array([6, 7]), sensors=[sensor1, sensor3])
robot4 = Robot.from_config(config1)
robot5 = Robot.from_config(config2)


# MOBILEROBOT — inherits from Robot, adds speed and movement

class Mobilerobot(Robot):
    def __init__(self, name, battery, position, sensors, speed):
        super().__init__(name, battery, position, sensors)
        self.speed = speed

    def move(self, direction):
        # direction passed at call time — not stored permanently
        print(f"{self.name} is moving at speed {self.speed} in direction {direction}")


# CLEANINGROBOT — inherits from Mobilerobot
# has everything Robot + Mobilerobot has plus cleaning mode

class Cleaningrobot(Mobilerobot):
    def __init__(self, name, battery, position, sensors, cleanmode, speed):
        super().__init__(name, battery, position, sensors, speed)
        self.cleanmode = cleanmode

    def start_cleaning(self):
        print(f"{self.name} is cleaning in {self.cleanmode} mode")


# ARMROBOT — inherits from Robot directly, adds joints

class Armrobot(Robot):
    def __init__(self, name, battery, position, sensors, num_joints):
        super().__init__(name, battery, position, sensors)
        self.num_joints = num_joints

    def move_joints(self, joint_id, angle):
        print(f"{self.name} moving {joint_id} to {angle} degrees")


# ROBOTFLEET — manages a collection of robot objects

class RobotFleet:
    def __init__(self):
        self.robots = []  # starts empty

    def add_robot(self, *robots):
        # *args — accepts any number of robots at once
        for robot in robots:
            self.robots.append(robot)

    def __str__(self):
        # prints fleet summary
        results = "Fleet summary\n"
        for robot in self.robots:
            results += f" - {robot.name} | {robot.battery}%\n"
        return results

    def get_active_robots(self):
        # list comprehension — returns robots with battery above 20
        return [robot for robot in self.robots if robot.battery >= 20]

    def get_lowest_battery(self):
        # lambda tells min() to compare by battery value
        return min(self.robots, key=lambda robot: robot.battery)

    def deploy_all(self):
        # isinstance check — only deploys cleaning robots
        for robot in self.robots:
            if isinstance(robot, Cleaningrobot):
                robot.start_cleaning()



# TEST CODE


# mobile robots
mobile_robot1 = Mobilerobot('delivery_robot', 70, np.array([3, 4]), sensors=[sensor1], speed=5)
mobile_robot2 = Mobilerobot('inspection_robot', 85, np.array([7, 8]), sensors=[sensor2], speed=3)
mobile_robot1.move('north')
mobile_robot2.move('east')

# cleaning robot
cleaning_robot1 = Cleaningrobot('cleaning_robot', 90, np.array([9, 10]), sensors=[sensor3], cleanmode='Zigzag', speed=4)
cleaning_robot1.start_cleaning()

# arm robot
arm_robot1 = Armrobot('assembly_arm', 80, np.array([11, 12]), sensors=[sensor1, sensor3], num_joints=6)
arm_robot1.display_info()
arm_robot1.move_joints('joint1', 45)

# comprehensions
all_sensors = [sensor1, sensor2, sensor3]
long_range = [s for s in all_sensors if s.sensor_range > 8]           # list comprehension
fleet_battery = {r.name: r.battery for r in [robot1, robot2, robot3]} # dict comprehension
fleet_sensors = {r.name: len(r.sensors) for r in [robot1, robot2, robot3]}

# display all robots
robot1.display_info()
robot2.display_info()
robot3.display_info()
robot4.display_info()
robot5.display_info()

robot1.active_sensors()

# dunder method tests
print(robot1)
print(repr(robot1))
print(robot1 == robot4)
print(len(robot1))

# property setter test
robot1.battery = 80
print(f"Battery valid: {Robot.validate_battery(robot1.battery)}")
print(f"Total robots created: {Robot.robot_count}")

# sensor logger test
print(sensor1.logger.get_stats())
print(f"Obstacle near sensor1: {sensor1.logger.detect_obstacle(2.0)}")

# isinstance and issubclass tests
print(isinstance(cleaning_robot1, Cleaningrobot))
print(isinstance(cleaning_robot1, Mobilerobot))
print(isinstance(cleaning_robot1, Robot))
print(isinstance(arm_robot1, Mobilerobot))
print(issubclass(Cleaningrobot, Mobilerobot))
print(issubclass(Armrobot, Mobilerobot))

# fleet tests
fleet = RobotFleet()
fleet.add_robot(robot1, robot2, robot3)
print(fleet)

active = fleet.get_active_robots()
for robot in active:
    print(robot.name)

lowest = fleet.get_lowest_battery()
print(f"Lowest battery: {lowest.name} at {lowest.battery}%")

fleet.add_robot(cleaning_robot1)
fleet.deploy_all()

# NumPy distance calculation
print(f"Distance robot1 to robot2: {robot1.distance_to(robot2):.2f}m")
print(f"Distance robot1 to robot3: {robot1.distance_to(robot3):.2f}m")

print(long_range)
print(fleet_battery)
print(fleet_sensors)




