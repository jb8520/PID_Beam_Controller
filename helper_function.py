def step_number_calc(angle) -> float:
    '''
    Returns the required `stepper.position` for angle `angle` in deg
    '''
    num_steps_cycle = 400
    num_microsteps_per_step = 32

    return float((angle / 360) * num_steps_cycle * num_microsteps_per_step)


def get_velocity(current_dist: float, previous_dist: float, dt: float) -> float:
    '''
    Returns the measured instantaneous velocity of the cart
    \n`dt`: seconds
    \n`distances`: cm
    '''

    velocity = (current_dist - previous_dist) / dt

    return velocity