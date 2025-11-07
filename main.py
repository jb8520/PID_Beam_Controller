from __init__ import *
from move_motor import move_to_angle

# ==== PID Controller Class ====
class PID:
    def __init__(
            self,
            dt: float,
            target: float,
            Kp: float,
            Ki: float,
            Kd: float
        ):

        self.dt = dt
        self.target = target

        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

        self.integral = 0
        self.prev_error = 0
    
    def update(self, error: float) -> tuple[float, float, float]:
        '''
        Returns a tuple of `(P, I, D)` values for an error `error`
        \n`get_integrand()` and `get_derivative()` implemented here
        '''
        
        P = self.Kp * error
        
        MAX_INTEGRAL = 20
        self.integral += error * self.dt
        self.integral = max(min(self.integral, MAX_INTEGRAL), -MAX_INTEGRAL)
        I = self.integral * self.Ki
        
        D = self.Kd * (error - self.prev_error) / self.dt
        
        self.prev_error = error

        return P, I, D

def get_error(current_distance: float, target: float) -> float:
    return target - current_distance

def update_target_location(pid: PID):
    '''
    Switches the target location for the oscillatory task
    '''
    target_1 = 9
    target_2 = 25
    pid.target = target_1 if pid.target == target_2 else target_2

    return pid


# ==== Define Parameters ====
target = 25 # target position: cm from detector
target_error = 1.0 # 'allowed' error from target: cm

MAX_ANGLE = 40 # deg

# PID coefficients

Kp, Ki, Kd = 2.0, 0.01, 2 # cart mass only
#Kp, Ki, Kd = 3, 0.01, 2 # cart + additional mass



if __name__ == '__main__':
    # ==== Initialize System ====
    current_distance = get_distance_us() # starting position
    previous_distance = 0

    start_time_us = ticks_us()
    previous_time_us = start_time_us

    dt = 0.01

    pid = PID(
        dt,
        target,
        Kp,
        Ki,
        Kd
    )


    print(current_distance)

    # ==== Iterates a counter used in naming of the csv file: easy run without writing over past data ====
    try:
        with open('pid_csv_counter.py', 'r') as c:
            csv_file_counter = int(c.read().strip())
    except FileNotFoundError:
        csv_file_counter = 0  # start at 0 if file doesn't exist
    with open('pid_csv_counter.py', 'w') as c:
        c.write(str(csv_file_counter + 1))

    # ==== Create and open .csv file to log data ====
    with open(f'data/pid_loop_data{csv_file_counter}.csv', 'w') as f:
        headers = ['elapsed_time', 'dt', 'P', 'I', 'D', 'error', 'distance', 'velocity']
        f.write(','.join(headers) + '\n')
    
        # ==== Iterate until object within 'acceptable' error from target ====
        counter = 0
        while counter < 1: # For the oscillatory target task, will oscillate for this many times. If `counter < 1`, this functionality is ignored and object will stop at the initial target location - no oscillation.

            while abs(get_error(current_distance, pid.target)) > target_error:
                # Time difference
                current_time_us: float = ticks_us()
                pid.dt = ticks_diff(current_time_us, previous_time_us) * 10**(-6)
                previous_time_us = current_time_us
                

                # Set angl
                error = get_error(current_distance, pid.target) # positive error needs beam angle to be positive (therefore beam goes down)
                P, I, D = pid.update(error)
                angle = P + I + D
                angle = max(min(angle, MAX_ANGLE), -MAX_ANGLE)
                #print(f'Error: {error}, Angle: {angle}, P: {P}, I: {I}, D: {D}')
                move_to_angle(angle)
                #sleep_ms(10)


                # Velocity calculation
                velocity = get_velocity(current_distance, previous_distance, pid.dt)
                previous_distance = current_distance

                # Elapsed time in seconds since start
                elapsed_time: float = ticks_diff(current_time_us, start_time_us) * 10**(-6)


                # Log measurement: elapsed_time, dt, error, distance, velocity
                f.write(f'{elapsed_time},{pid.dt},{P},{I},{D},{error},{current_distance},{velocity}\n')


                # Measure distance
                current_distance = get_distance_us() # distance via us sensor
                #current_dist = get_distance_ir() # distance via ir sensor
            
            counter += 1
            pid = update_target_location(pid)
        
        move_to_angle(0)

        # Record additional data points
        sleep_ms(10)

        for i in range(100):
            # Time difference
            current_time_us: float = ticks_us()
            pid.dt = ticks_diff(current_time_us, previous_time_us) * 10**(-6)
            previous_time_us = current_time_us

            # Velocity calculation
            velocity = get_velocity(current_distance, previous_distance, pid.dt)
            previous_distance = current_distance

            # Elapsed time in seconds since start
            elapsed_time: float = ticks_diff(current_time_us, start_time_us) * 10**(-6)


            # Log measurement: elapsed_time, dt, error, distance, velocity
            f.write(f'{elapsed_time},{pid.dt},0,0,0,{get_error(current_distance, pid.target)},{current_distance},{velocity}\n')

            
            # Measure distance
            current_distance = get_distance_us() # distance via us sensor
            sleep_ms(10)
        

        sleep_ms(1000)
        print(f'Final distance: {get_distance_us()}\nTarget distance: {target}')