import numpy as np
a=np.array([0,1,2,3,4,5,6,7,8,9])
b=np.zeros((3,3))
c=np.ones((3,3))
d=np.arange(0,10,2)
print(a)
print(b)
print(c)
print(d)

print(a.shape)
print(b.shape)
print(c.shape)
print(d.shape)

print(a.dtype)
print(b.dtype)
print(c.dtype)
print(d.dtype)

print(a.ndim)
print(b.ndim)
print(c.ndim)
print(d.ndim)

a = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90])

print(a[0:3])
print(a[-3:10])
print(a[::2])
print(a[2:5])
b = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])

print(b[0,:])
print(b[:,1])
print(b[0:2,0:2])

a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])

print(a+b)
print(a*2)
print(b*10)
print(a**2)

print(np.sum(a))
print(np.mean(a))
print(np.max(b))
print(np.min(b))
print(np.std(a))

A = np.array([[1, 2],
              [3, 4]])

B = np.array([[5, 6],
              [7, 8]])

print(A@B)
print(A*B)

# ============================================================
# NumPy applied to robotics
# ============================================================

robot_pos1=np.array([0,9,66])
robot_pos2=np.array([5,8,8])
print(np.linalg.norm(robot_pos1 - robot_pos2))

sensor_readings=np.random.uniform(0.5,10.0,10)
print(np.mean(sensor_readings))
print(np.max(sensor_readings))
print(np.min(sensor_readings))

print(sensor_readings[sensor_readings<2.0])

angle=np.radians(90)
R=np.array([[np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)]])
v=np.array([1,0])
rotated=R@v
print(rotated)
