import odrive
import time

class ODriveMotorCalibrator:
    def __init__(self):
        """Initialize ODrive and set up axes."""
        self.odrv0 = odrive.find_any()
        self.axis0 = self.odrv0.axis0
        self.axis1 = self.odrv0.axis1

    def calibrate_axis(self, axis):
        """Calibrate a specified axis."""
        # Start full calibration sequence
        axis.requested_state = 3  # AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        time.sleep(15)  # Wait for calibration to complete
        
        # Set controller to closed-loop control
        axis.requested_state = 8  # AXIS_STATE_CLOSED_LOOP_CONTROL

        # Configure controller settings
        axis.controller.config.input_mode = 3  # POS_FILTER
        axis.controller.config.input_filter_bandwidth = 1
        axis.controller.config.control_mode = 3  # POSITION_CONTROL
        axis.controller.config.vel_limit = 5
        axis.controller.config.vel_gain = 0.165

        # Return the encoder position estimate
        return axis.encoder.pos_estimate

    def calibrate_all(self):
        """Calibrate both axes."""
        pos0 = self.calibrate_axis(self.axis0)
        pos1 = self.calibrate_axis(self.axis1)
        return pos0, pos1

    def dump_errors(self):
        """Check and print errors."""
        # This function needs to be defined or implemented if it is to be used.
        # Example: print(self.odrv0.axis0.error)
        pass

    def start_live_plotter(self):
        """Placeholder for live plotting function."""
        # This function needs to be defined or implemented if it is to be used.
        # Example: start_liveplotter(lambda: [self.axis0.encoder.pos_estimate, self.axis0.controller.pos_setpoint])
        pass

    def print_positions(self):
        """Continuously print the positions of both axes."""
        while True:
            pos0 = self.axis0.encoder.pos_estimate
            pos1 = self.axis1.encoder.pos_estimate
            print(f"Axis 0 Position: {pos0:.2f}\tAxis 1 Position: {pos1:.2f}")
            time.sleep(1)  # Delay to prevent spamming the console

if __name__ == "__main__":
    calibrator = ODriveMotorCalibrator()
    calibrator.calibrate_all()
    calibrator.print_positions()
