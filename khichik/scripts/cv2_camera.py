import time
import cv2
from picamera2 import Picamera2


class Camera:
    '''
    Thin wrapper around Picamera2 to make it look like a PiCamera
    Compatible with Pi Camera Module 3 on Raspberry Pi OS Bullseye+
    '''

    def __init__(self):
        self.picam2 = Picamera2()

        # Configure for still captures (you can change resolution if needed)
        config = self.picam2.create_still_configuration(main={"size": (1600, 1200)})
        self.picam2.configure(config)
        self.picam2.start()

        time.sleep(0.5)  # allow auto-exposure to adjust
        self.previewing = False

    def start_preview(self):
        """Start preview (no-op here, handled in test)"""
        self.previewing = True

    def stop_preview(self):
        """Stop preview"""
        self.previewing = False

    def capture(self, filename, resize=None):
        """
        Capture an image and save to file
        resize is not supported
        """
        frame = self.picam2.capture_array()
        cv2.imwrite(filename, frame)

    def close(self):
        """Release the camera"""
        self.picam2.stop()


# Alias to mimic picamera API
PiCamera = Camera


def test():
    """Test function: show live preview"""
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"size": (640, 480)})
    picam2.configure(config)
    picam2.start()

    print('Press "q" to quit preview')
    while True:
        frame = picam2.capture_array()
        cv2.imshow("PiCam3 Preview", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    picam2.stop()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    test()

