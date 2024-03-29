import time

import RPi.GPIO as GPIO


# Our class for the stepper motor of our receiver pi
class StepperMotor:
    def __init__(self):
        self.__pins = [17, 27, 18, 22]  # Save pins

        # Save step sequence
        self.__STEP_SEQUENCE = (
            (1, 0, 0, 1),
            (1, 0, 0, 0),
            (1, 1, 0, 0),
            (0, 1, 0, 0),
            (0, 1, 1, 0),
            (0, 0, 1, 0),
            (0, 0, 1, 1),
            (0, 0, 0, 1),
        )

        self.pins_reversed = self.__pins[::-1]  # Reverse the pins
        self.sequence_reversed = self.__STEP_SEQUENCE[::-1]  # Reverse the sequence

        GPIO.setwarnings(False)  # Mute warnings
        GPIO.setmode(GPIO.BCM)  # Set GPIO mode to BOARD

        # Set pins in the list to output
        for pin in self.__pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)

        self.__delay_after_step = 1 / 400  # Delay after each step in Hz
        self.debug_mode = False  # Boolean for some debug messages

    # Function to do a step forward
    def do_clockwise_step(self, steps):
        counter = 0
        for step in range(steps):
            if self.debug_mode: print(f"Step {step + 1}: ")
            for pin in range(len(self.__pins)):
                GPIO.output(self.__pins[pin], self.__STEP_SEQUENCE[counter][pin])
                if self.debug_mode: print(f"Set pin {self.__pins[pin]} to {self.__STEP_SEQUENCE[counter][pin]}.")
            counter = (counter + 1) % len(
                self.__STEP_SEQUENCE)  # Calculate the difference between both positive numbers
            time.sleep(self.__delay_after_step)

    # Function to do a step backward
    def do_counterclockwise_step(self, steps):
        counter = 0
        for step in range(steps):
            if self.debug_mode: print(f"Step {step + 1}: ")
            for pin in range(4):
                GPIO.output(self.__pins[pin], self.__STEP_SEQUENCE[counter][pin])
                if self.debug_mode: print(f"Set pin {self.__pins[pin]} to {self.__STEP_SEQUENCE[counter][pin]}.")
            counter = (counter - 1) % len(self.__STEP_SEQUENCE)  # Calculate the rest of the division
            time.sleep(self.__delay_after_step)

    # Function to move the motor clockwise by degrees
    def do_clockwise_degrees(self, degrees):
        steps = int(degrees / (5.625 / 64))
        self.do_clockwise_step(steps)

    # Function to move the motor counterclockwise by degrees
    def do_counterclockwise_degrees(self, degrees):
        steps = int(degrees / (5.625 / 64))
        self.do_counterclockwise_step(steps)

    # Function to clean up all pins
    def clean_up_gpio(self):
        for pin in self.__pins:
            GPIO.output(pin, 0)
        GPIO.cleanup()
        print("Cleaned up all pins.")
