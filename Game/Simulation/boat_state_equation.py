import numpy as np
import yaml
from typing import List

params = open('params.yaml')
params_dict = yaml.safe_load(params)
# SET BOAT CONSTANTS
DRIFT_COEFF = params_dict['boat']['drift_coef']
TAN_FRICTION = params_dict['boat']['tan_friction']
ANG_FRICTION = params_dict['boat']['ang_friction']
SAIL_LIFT = params_dict['boat']['sail_lift']
RUDDER_LIFT = params_dict['boat']['rudder_lift']
DIST_TO_SAIL = params_dict['boat']['dist_to_sail']
DIST_TO_MAST = params_dict['boat']['dist_to_mast']
DIST_TO_RUDDER = params_dict['boat']['dist_to_rudder']
MASS = params_dict['boat']['mass']
MOI = params_dict['boat']['moi']
RUDDER_BREAK_COEF = params_dict['boat']['rudder_break_coef']
# SET ENVIRONMENT CONSTANTS
TRUE_WIND_ANGLE = params_dict['environment']['true_wind_angle']
TRUE_WIND_SPEED = params_dict['environment']['true_wind_speed']
# SET SIMULATION CONSTANTS
dt = params_dict['simulation']['simulation_step']
#Set indexes (indecies)
X = 0        #X position          [m]          
Y = 1        #Y position          [m]   
THETA =2     #Heading ange        [rad]
V = 3        #Boat speed          [m/s]
W = 4        #Boat angular speed  [rad/s]   


#Temporary solution, until ROS control is established
sail_angle =  0.2
rudder_angle = 0.1

def calculate_change(state: List[float])-> List[float]:

    tangent_apparent_wind = TRUE_WIND_SPEED * np.cos(TRUE_WIND_ANGLE - state[THETA]) - state[V]
    normal_apparent_wind = TRUE_WIND_SPEED * np.sin(TRUE_WIND_ANGLE - state[THETA])
    apparent_wind_angle = np.arctan2(normal_apparent_wind,tangent_apparent_wind)
    apparent_wind_speed = np.sqrt(tangent_apparent_wind**2 + normal_apparent_wind**2)

    sigma = np.cos(apparent_wind_angle) + np.cos(sail_angle)
    if sigma < 0:
        delta_s = np.pi + apparent_wind_angle
    else:
        delta_s = -np.sign(np.sin(apparent_wind_angle)) * sail_angle

    rudder_force = RUDDER_LIFT * state[V] * np.sin(rudder_angle)
    sail_force = SAIL_LIFT * apparent_wind_speed * np.sin(delta_s - apparent_wind_angle)

    dx = state[V] * np.cos(state[THETA]) + DRIFT_COEFF * TRUE_WIND_SPEED * np.cos(TRUE_WIND_ANGLE)
    dy = state[V] * np.sin(state[THETA]) + DRIFT_COEFF * TRUE_WIND_SPEED * np.sin(TRUE_WIND_ANGLE)
    dtheta = state[W]
    dv = (sail_force * np.sin(delta_s) - rudder_force * np.sin(rudder_angle) - TAN_FRICTION * state[V]**2) / MASS
    dw = (sail_force * (DIST_TO_SAIL - DIST_TO_MAST * np.cos(delta_s)) - DIST_TO_RUDDER * rudder_force * np.cos(rudder_angle) - ANG_FRICTION * state[W] * state[V]) / MOI
    return [dx,dy,dtheta,dv,dw]

def solve_euler(state: List[float])-> List[float]:
    d = calculate_change(state)
    state[X] += d[X] * dt
    state[Y] += d[Y] * dt
    state[THETA]  = (state[THETA] + d[THETA] * dt) % (2 * np.pi) #ensuring that theta is between 0 and 2*pi
    state[V] += d[V] * dt
    state[W] += d[W] * dt
    return state

