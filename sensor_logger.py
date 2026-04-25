import numpy as np
class SensorDataLogger:
    def __init__(self):
        self.readings=np.array([])

    def add_reading(self, value):
        self.readings =np.append(self.readings,value)
    
    def get_stats(self):
        return {
            "mean": np.mean(self.readings),
            "std": np.std(self.readings),
            "min": np.min(self.readings),
            "max": np.max(self.readings)
        }
    def detect_obstacle(self, threshold):
        return np.any(self.readings < threshold)  

logger = SensorDataLogger()
lidar_logger=SensorDataLogger()
readings=np.random.uniform(0.5,10,100)
for reading in readings:
    lidar_logger.add_reading(reading)

print(f"Total readings : {len(lidar_logger.readings)}")
print(f"Status : {lidar_logger.get_stats()}")
print(f"obstacle detected : {lidar_logger.detect_obstacle(1.5)}")
logger.add_reading(5.2)
logger.add_reading(3.1)
logger.add_reading(8.7)
print(logger.readings)
print(logger.get_stats())
print(logger.detect_obstacle(4.0))

np.save('lidar_readings.npy' , lidar_logger.readings)
print("Readings saved to lidar_readings.npy")
loaded_readings=np.load('lidar_readings.npy')
print(f"Loaded {len(loaded_readings)} readings from file")
print(f"first 5 :{loaded_readings[:5]}")