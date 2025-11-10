from packages import *
from Helpers import *


# Change starting angle of motor
angle = -25

move_to_angle(angle)

start_time_us = ticks_us()
current_distance = get_distance_us()

with open(f'data/data_{angle}.csv', 'w') as f:
    headers = ['elapsed_time', 'distance']
    f.write(','.join(headers) + '\n')
    
    while current_distance > 5.0: # 5 is an arbitrary distance from edge, data recorded won't involve cart hitting edge
        # Elapsed time in seconds since start
        current_time_us: float = ticks_us()
        elapsed_time: float = ticks_diff(current_time_us, start_time_us) * 10**(-6)
            
        # Measure distance
        current_distance = get_distance_us() # distance via us sensor
                    
        f.write(f'{elapsed_time},{current_distance}\n')

move_to_angle(0)