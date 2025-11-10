from packages import *
from Helpers import *



# ==== Initialize Stepper ====
stepper = Stepper()

# Set stepper velocity and acceleration
stepper.velocity = 1000
stepper.acceleration = 1300



def loop_through_sine(amplitude_deg: int = 40, periods: int = 5, step: float = 0.2) -> None:
    '''
    Measures the position and velocity of the cart over a sinusoidal motor pattern
    '''

    # ==== Iterates a counter used in naming of the csv file: easy run without writing over past data ====
    try:
        with open('sine_csv_counter.py', 'r') as c:
            csv_file_counter = int(c.read().strip())
    except FileNotFoundError:
        csv_file_counter = 0  # start at 0 if file doesn't exist
    with open('sine_csv_counter.py', 'w') as c:
        c.write(str(csv_file_counter + 1))

    # ==== Create and open .csv file to log data ====
    with open(f'data/sine_loop_data{csv_file_counter}.csv', 'w') as f:
        headers = ['elapsed_time', 'distance', 'velocity']
        f.write(','.join(headers) + '\n')
    
        # ==== Set Parameters ====
        start_time_us: float = ticks_us()
        
        previous_time_us = 0.0
        previous_dist = 0.0
        
        max_range = 2 * pi * periods

        # ==== Iterate over theta values in a sinusoidal pattern: range only takes int so *10 factor ====
        for i in range(0, int(10 * max_range), int(10 * step)):
            theta = - amplitude_deg * sin(i / 10)
            
            # Move Motor
            move_to_angle(theta)
            sleep_ms(40)

            # Measure distance and velocity
            current_dist = get_distance_us() # distance via us sensor
            #current_dist = get_distance_ir() # distance via ir sensor
            current_time_us: float = ticks_us()

            # Time difference
            dt: float = ticks_diff(current_time_us, previous_time_us) * 10**(-6)
            previous_time_us = current_time_us

            # Velocity calculation
            velocity = get_velocity(current_dist, previous_dist, dt)
            previous_dist = current_dist

            # Elapsed time in seconds since start
            elapsed_time: float = ticks_diff(current_time_us, start_time_us) * 10**(-6)
                    
            # Log measurement
            f.write(f'{elapsed_time},{current_dist},{velocity}\n')
        
        # Return to zero
        stepper.position = 0



if __name__ == '__main__':
    loop_through_sine()