#----- Packages used to control the motor and measure the distance of the cart along the beam -----
from stepper_driver.stepper_tmcm import Stepper   # type: ignore

from ir_sensor.vl53l4x import VL53L4Cx   # type: ignore
from machine import Pin, UART   # type: ignore


#----- Helper Functions -------
class CircularBuffer:
    """
    Fixed size storage (buffer) which deletes oldest value to make room for new incoming values. Used to store latest N recorded values.
    """

    def __init__(self, size):
        self._len = size  # Size of buffer.
        self._buf = [None] * self._len
        self._end = 0  # End of buffer.

    def __len__(self):
        return self._len

    def __getitem__(self, key):
        return self.get(key)

    def push(self, *data):
        """
        Append data to the end of the buffer.
        """

        data = data[0] if len(data) == 1 else tuple(data)
        self._buf[self._end] = data
        self._end = (self._end + 1) % self._len

    def get(self, index: int):
        """
        The oldest value is available at index 0 and the newest value is available at index -1 i.e., get(-1)
        """

        return self._buf[(self._end + index) % self._len]