# BeamBalancer

BeamBalancer is a MicroPython-powered PID control system designed for the Raspberry Pi Pico. It actively controls the tilt of a physical beam using a motor-driven linkage, allowing the system to roll an object (like a ball or cart) to a desired target position from anywhere along the beam.

The system uses either an infrared (IR) sensor or ultrasonic sensor to measure the distance of the object along the beam, feeding this data into a PID controller that constantly adjusts the beam angle for smooth, stable movement.

BeamBalancer also includes an automatic tuning module, `pid_auto_tuner.py`, that uses the *Ziegler–Nichols* method to estimate optimal PID parameters (Kp, Ki, Kd) based on your physical setup.



## Why Use BeamBalancer?
If you're working on control systems, robotics, embedded engineering, or just want a hands-on project that actually moves something based on real-time feedback, this is a perfect base system.



## **BeamBalancer** gives you:

- A clean reference implementation of a PID loop in MicroPython
- Real-world sensor integration (IR or ultrasonic)
- Motor angle actuation via linkage
- Optional auto-tuning
- A physically intuitive system that’s easy to experiment with

And let’s be real, balancing a ball with a microcontroller is just cool.



## Features

BeamBalancer packs a bunch of useful components for building and experimenting with control loops:

- ⚙️ PID control loop (tunable Kp, Ki, Kd)

- 🎯 Position targeting — move the object to any point along the beam

- 📡 Support for both IR or ultrasonic distance sensors (adjust to fit your physical system)

- 🔄 Motor actuation via a linkage system

- 🔍 Optional *Ziegler–Nichols* auto-tuner (pid_auto_tuner.py)

- 💿 Recorded data is automatically saved as .csv files (in the `./Data` folder) that can be used to plot outputs



## How It Works (Quick Overview)
- The sensor continuously measures the position of the object on the beam.
- The PID controller compares the current position to the desired target.
- Based on the error, it calculates a correction using the PID equation.
- The motor rotates through a linkage, adjusting the beam’s tilt.
- The object rolls accordingly, closing the loop.

The auto-tuner can vibrate/oscillate the system to determine the “ultimate gain” and “ultimate period,” then compute suggested PID values.



## Getting Started

### Prerequisites

- Raspberry Pi Pico
- MicroPython firmware installed
- IR distance sensor or ultrasonic distance sensor (exact implementation may vary based on available sensors)
- Servo or DC motor with motor driver (depending on your design)
- Linkage system attaching the motor to the beam
- An object to roll such as a ball or cart
- Thonny or any MicroPython uploader
- Necessary packages based on your exact system



### Installation

Flash MicroPython to the Pico if you haven't already.

Clone the project to your machine:

```bash
git clone https://github.com/yourusername/beambalancer.git
cd beambalancer
```

Copy the files over to your Pico. You can do this easily through Thonny or mpremote.



## Usage

Configure the system to match your exact setup.
Once variables such as the desired target location are specified, run `main.py` to activate the object to target motion. Please note, the PID coefficients need to be set for this to work; either via manual or automatic tuning.

There is also an additional sinusoidal motion demonstration available via `sinusoidal_motion.py`.


If you want Ziegler–Nichols recommended PID values, run the file `pid_auto_tuner.py`.

This will:
- Oscillate the system
- Calculate ultimate gain + period
- Print recommended Kp, Ki, Kd values



## Project Structure
File Tree:

```graphql
.
├── Data/                       # output csv data files
│
├── Helpers/                    # modular hardware helper scripts
│   ├── __init__.py
│   ├── distance_ir.py          # IR distance measurement
│   ├── distance_us.py          # ultrasonic distance measurement
│   ├── move_motor.py           # motor/servo control logic
│   └── other.py                # misc utilities
│
├── investigation.py            # manual investigation of system behaviour
├── micros_lab.py               # microcontroller utilities (stepper control, IR sensor setup, CircularBuffer helper)
├── main.py                     # main PID system
├── packages.py                 # imports/package management for system
├── pid_auto_tuner.py           # Ziegler–Nichols PID auto-tuning
├── pid_csv_counter.py          # counter for PID output csv naming convention
├── sine_csv_counter.py         # counter for sinusoidal motion output csv naming convention
├── sinusoidal_motion.py        # generates sinusoidal motor movement
│
├── README.md
└── LICENSE
```



## Tuning & Calibration
- BeamBalancer will need to be tweaked to your exact physical components. However due to the modular and clean design, this should be trivial.
- The beam should initially be zeroed (assumed to be horizontally level)
- Ensure your sensor readings are stable
- Check the linkage motion range
- Make sure the object rolls freely
- Running the auto-tuner is highly recommended unless you already know your PID values.



## Contributing

Pull requests, improvements, and feature suggestions are welcome!
If you add support for new sensors or motor drivers, please document them.



## License

GNU AFFERO GENERAL PUBLIC LICENSE Version 3, © jb8520, James Boss
