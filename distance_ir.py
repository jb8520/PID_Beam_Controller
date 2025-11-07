from micros_lab import *

# ==== Distance sensor logic ====
ir_sensor_timing_budget_in_ms = 40

irsensor = VL53L4Cx()
irsensor.timing_budget = ir_sensor_timing_budget_in_ms
irsensor.start_ranging() # tells the sensor to start measuring
# pin which signals when a measurement is available
measurement_available_pin = Pin(14, mode = Pin.IN, pull = Pin.PULL_UP)


def get_distance_ir() -> float:
    '''
    Returns the measured distance from the (infrared) sensor to the cart
    \n Raises `ValueError` if measured distance exceeds its maximum value
    '''
    # Wait until measurement available
    while measurement_available_pin.value() == 1: 
        continue

    distance = irsensor.distance
    
    irsensor.clear_interrupt()

    if distance > 39.0: # 1 more than measured max separation between sensor and cart
        raise ValueError('Measured distance is off the beam.')
        
    return distance



if __name__ == '__main__':
    print(get_distance_ir())