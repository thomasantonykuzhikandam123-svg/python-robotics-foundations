class Sensors:
    def __init__(self, sensor_type, sensor_range, sensor_status):
        self.sensor_type = sensor_type
        self.sensor_range = sensor_range
        self.sensor_status = sensor_status

    def status_report(self):
        print(f"Sensor Type: {self.sensor_type}")
        print(f"Range: {self.sensor_range}")
        print(f"Status: {self.sensor_status}")


sensor1 = Sensors('ultrasonic', 7.5, 'Active')
sensor2 = Sensors('camera', 10, 'Inactive')
sensor3 = Sensors('lidar', 15, 'Active')


class Robot:
    robot_count = 0

    def __init__(self, name, battery, position, sensors):
        self.name = name
        self.battery = battery
        self.position = position
        self.sensors = sensors
        Robot.robot_count += 1

    def active_sensors(self):
        active = [sensor for sensor in self.sensors if sensor.sensor_status == 'Active']
        print(f"Active sensors on {self.name}:")
        for sensor in active:
            print(f"  - {sensor.sensor_type} | {sensor.sensor_range}m")

    def display_info(self):
        print(f"Robot: {self.name}")
        print(f"Battery: {self.battery}")
        print(f"Position: {self.position}")
        print("Sensors:")
        for sensor in self.sensors:
            print(f"  - type: {sensor.sensor_type} | range: {sensor.sensor_range} | status: {sensor.sensor_status}")
        print()

    @classmethod
    def from_config(cls, config_dict):
        name = config_dict['name']
        battery = config_dict['battery']
        position = config_dict['position']
        sensors = config_dict['sensors']
        return cls(name, battery, position, sensors)
    @staticmethod
    def validate_battery(battery):
        if battery >= 0 and battery <= 100:
            return True
        else:
            return False


config1 = {
    'name': 'picking_robot',
    'battery': 100,
    'position': '{2,3}',
    'sensors': [sensor1, sensor2]
}

config2 = {
    'name': 'assembly_robot',
    'battery': 90,
    'position': '{4,5}',
    'sensors': [sensor2, sensor3]
}

robot1 = Robot('warehouse_robot', 100, '{0,0}', sensors=[sensor1, sensor2])
robot2 = Robot('robotic_arm', 80, '{5,6}', sensors=[sensor3])
robot3 = Robot('mining_robot', 60, '{6,7}', sensors=[sensor1, sensor3])
robot4 = Robot.from_config(config1)
robot5 = Robot.from_config(config2)

class Mobilerobot(Robot):
    def __init__(self,name,battery,position,sensors,speed):
        super().__init__(name,battery,position,sensors)
        self.speed=speed
    
    def move(self, direction):
        print(f"{self.name} is moving at a speed of {self.speed} in direction {direction}")
class Cleaningrobot(Mobilerobot):
    def __init__(self,name,battery,position,sensors,cleanmode,speed):
        super().__init__(name,battery,position,sensors,speed)
        self.cleanmode=cleanmode
    def start_cleaning(self):
        print(f"{self.name} is cleaning in {self.cleanmode} mode")
    
class Armrobot(Robot):
    def __init__(self,name,battery,position,sensors,num_joints):
        super().__init__(name,battery,position,sensors)
        self.num_joints=num_joints
    def move_joints(self,joint_id,angle):
        print(f"{self.name} with {joint_id} is moving in {angle} degree angle")
mobile_robot1=Mobilerobot('delivery_robot',70,'{3,4}',sensors=[sensor1],speed=5)
mobile_robot2=Mobilerobot('inspection_robot',85,'{7,8}',sensors=[sensor2],speed=3)   
mobile_robot1.move('north')
mobile_robot2.move('east') 
cleaning_robot1=Cleaningrobot('cleaning_robot',90,'{9,10}',sensors=[sensor3],cleanmode='Zigzag',speed=4)
cleaning_robot1.start_cleaning()
arm_robot1=Armrobot('assembly_arm',80,'{11,12}',sensors=[sensor1,sensor3],num_joints=6)
arm_robot1.display_info()
arm_robot1.move_joints('joint1',45)
robot1.display_info()
robot2.display_info()
robot3.display_info()
robot4.display_info()
robot5.display_info()

robot1.active_sensors()
print(f"Is {robot1.name}'s battery valid? {Robot.validate_battery(robot1.battery)}")


print(f"Total robots created: {Robot.robot_count}")
print(isinstance(cleaning_robot1, Cleaningrobot))
print(isinstance(cleaning_robot1, Mobilerobot))
print(isinstance(cleaning_robot1, Robot))
print(isinstance(arm_robot1, Mobilerobot))
print(issubclass(Cleaningrobot, Mobilerobot))
print(issubclass(Armrobot, Mobilerobot))

