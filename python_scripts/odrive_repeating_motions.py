import odrive
import time

class ODrivePositionController:
    def __init__(self):
        """Initialize ODrive and set up axis."""
        self.odrv0 = odrive.find_any()
        self.axis0 = self.odrv0.axis0

    def configure_controller(self, filter_bandwidth=5):
        """Configure the controller's input filter bandwidth."""
        self.axis0.controller.config.input_filter_bandwidth = filter_bandwidth

    def set_initial_position_bounds(self, offset=0.25):
        """Set initial position bounds based on current position."""
        self.pos = self.axis0.encoder.pos_estimate
        time.sleep(1)
        self.max_pos = self.pos + offset
        self.min_pos = self.pos - offset
        print(f"Initial position: {self.pos}")

    def start_position_control(self, step_size=0.5, position_threshold=0.05):
        """Continuously adjust the position of the axis within bounds."""
        n = step_size
        count = 0

        while True:
            time.sleep(0.25)
            self.pos = self.axis0.encoder.pos_estimate
            print(f"Current position: {self.pos}")
            self.axis0.controller.input_pos = self.pos + n

            if self.axis0.encoder.pos_estimate > self.max_pos - position_threshold:
                n = -step_size
            elif self.axis0.encoder.pos_estimate < self.min_pos + position_threshold:
                n = step_size

if __name__ == "__main__":
    controller = ODrivePositionController()
    controller.configure_controller()
    controller.set_initial_position_bounds()
    controller.start_position_control()
