from __init__ import *
from main import PID, get_error
from move_motor import move_to_angle

class PIDAutoTuner:
    def __init__(self, pid, target: float, max_angle: int = 35):
        self.pid = pid
        self.move_fn = move_to_angle
        self.distance_fn = get_distance_us
        self.target = target
        self.MAX_ANGLE = max_angle

    def find_ultimate_gain(self):
        Kp = 0.1
        Ki = 0
        Kd = 0
        oscillations = []
        print("Starting Ku search...")

        while Kp < 10:
            self.pid.Kp = Kp
            self.pid.Ki = Ki
            self.pid.Kd = Kd
            stable = self.run_test()
            
            if stable:
                Kp += 0.1
            
            else:
                # Found oscillation threshold
                Tu = self.estimate_period(oscillations)
                print(f"Found Ku = {Kp}, Tu = {Tu}")
                return Kp, Tu
        
        return None, None

    def run_test(self, duration: float = 5.0):
        start = ticks_ms()
        history = []

        while (ticks_ms() - start) / 1000 < duration:
            dist = self.distance_fn()
            error = get_error(dist, self.target)
            P, I, D = self.pid.update(error)
            angle = P + I + D
            angle = max(min(angle, self.max_angle), -self.max_angle)
            self.move_fn(angle)
            history.append(error)
            sleep_ms(20)
        
        return self.check_oscillations(history)

    def check_oscillations(self, err_list):
        # crude: detect sign changes in error to see if oscillating
        signs = [e > 0 for e in err_list]
        crossings = sum(signs[i] != signs[i-1] for i in range(1, len(signs)))
        
        return crossings > 4  # more than 2 oscillations

    def estimate_period(self, err_list):
        # crude period estimate from zero-crossings
        zero_crossings = []
        for i in range(1, len(err_list)):
            if err_list[i-1] * err_list[i] < 0:
                zero_crossings.append(i)
        if len(zero_crossings) < 2:
            return None
        
        avg_period = (zero_crossings[-1] - zero_crossings[0]) / (len(zero_crossings) - 1)
        
        return avg_period * 0.02  # assuming 20ms per sample



if __name__ == '__main__':
    pid_auto_tuner = PIDAutoTuner(
        pid = PID,
        target = 11.0
    )

    Ku, Tu = pid_auto_tuner.find_ultimate_gain()
    if Ku and Tu:
        Kp = 0.6 * Ku
        Ki = 1.2 * Kp / Tu
        Kd = 0.075 * Kp * Tu

        print(f'Kp: {Kp}\n Ki: {Ki}\n Kd: {Kd}')
    
    else:
        print('Could not find valid values!')