import time
from time import sleep

import cv2

from cvdarts.darts_detector import get_new_images


def is_frame_at_frame_rate(frame_rate: int, time_elapsed: int) -> object:
    return time_elapsed > 1. / frame_rate


class GameLoop:
    """
    GameLoop controls the application flow. It provides the clock speed of the application by setting a frame rate
    for the capturing devices. While running, the game loop queries the devices in the resulting time periods and
    delegates the results from the capturing devices to the processing functions.
    """

    def __init__(self, devices):
        """
        :param devices: capturing devices (e.g. web cams) for capturing visual input
        :type devices: list of CapturingDevice
        """
        self.devices = devices
        self.capturing = True
        self.frames_per_second = 2

    def run(self):
        """
        runs the game loop
        """
        prev = 0

        while self.capturing:
            time_elapsed = time.time() - prev
            # TODO find a way to free cpu time (non-blocking) and remove sleep
            sleep(0.2)
            if is_frame_at_frame_rate(self.frames_per_second, time_elapsed):
                prev = time.time()

                self.capture_images()
                captured_input_of_all_devices = get_new_images(self.devices)
                counter = 0
                for captured_input in captured_input_of_all_devices:
                    counter += 1
                    if captured_input != []:
                        cv2.imshow('device_' + str(counter), captured_input)
                        cv2.waitKey(1)

        # When everything done, release the capture
        for captured_input in self.devices:
            captured_input.release()

        cv2.destroyAllWindows()

    def capture_images(self):
        for device in self.devices:
            device.process_image()