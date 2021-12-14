from boat_state_equation import *
import matplotlib.pyplot as plt


x_array = []
y_array = []
theta_array = []
v_array = []
w_array = []
time_array = []
i = 0
boat = [0,0,np.pi/2,0,0]
def get_true_wind_coords(angle: float = TRUE_WIND_ANGLE,speed: float = TRUE_WIND_SPEED):
    true_wind_x = speed * np.cos(angle)
    true_wind_y = speed * np.sin(angle)
    return true_wind_x,true_wind_y
while i < 100:
    x_array.append(boat[X])
    y_array.append(boat[Y])
    theta_array.append(boat[THETA])
    v_array.append(boat[V])
    w_array.append(boat[W])
    time_array.append(i)
    boat = solve_euler(boat)
    i += dt

plt.figure()
plt.plot(x_array,y_array)
plt.title("Droga")
plt.arrow(0,0,get_true_wind_coords()[0],get_true_wind_coords()[1],color = 'red',width = 1)
plt.axis('equal')
plt.figure()
plt.plot(time_array,theta_array)
plt.title('theta(t)')
plt.figure()
plt.plot(time_array,v_array)
plt.title('v(t)')
plt.figure()
plt.plot(time_array,w_array)
plt.title('w(t)')
plt.show()