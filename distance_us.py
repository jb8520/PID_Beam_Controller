from micros_lab import *

# ==== Distance sensor logic ====
# Trigger ultrasonic pulse pin
trigger = Pin(2, mode = Pin.OUT) # trigger to sensor 
# Get distance from ultrasonic sensor pin
echo = Pin(3, mode = Pin.IN)


def get_distance_us() -> float:
    '''
    Returns the measured distance from the (ultrasonic) sensor to the cart
    \n Raises `ValueError` if measured distance exceeds its maximum value
    '''

    speed_sound_air = 340.0 # m/s
    
    trigger.on()
    
    sleep_us(10)
    
    trigger.off()
    
    while echo.value() == 0: 
        continue

    t0 = ticks_us()
        
    while echo.value() == 1:
        continue
    
    t1 = ticks_us()
        
    time_diff = ticks_diff(t1, t0) * 10**(-6)

    distance = speed_sound_air * 100 * time_diff / 2
    
    if distance > 45.0: # 1 more than measured max separation between sensor and cart
        raise ValueError('Measured distance is off the beam.')
        
    return distance

if __name__ == '__main__':
    print(get_distance_us())