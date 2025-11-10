from packages import *
from . import step_number_calc

# ==== Initialize Stepper ====
stepper = Stepper()

stepper.velocity = 1000
stepper.acceleration = 1300




def move_to_angle(angle) -> None:
    '''
    Moves motor to angle `angle` (deg)
    \n\+ angle: clockwise
    '''

    stepper.position = step_number_calc(angle)


def move_motor(start_angle: int = -400, end_angle: int = 400, interval: int = 5) -> None:
    '''
    Moves motor from `start_angle` to `end_angle`, in intervals of `interval`
    \nRange only takes int, so input params * 10
    '''
    
    for deg in range(start_angle, end_angle, interval):
        move_to_angle(deg / 10)
        
        sleep_ms(100) # 0.1s



if __name__ == '__main__':
    move_motor(0)