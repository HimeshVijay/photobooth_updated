import time
import cv2
import numpy as np
from picamera2 import Picamera2


class DummyPreview:
    """Fake preview object to mimic PiCamera API."""
    def __init__(self):
        self.fullscreen = False
        self.window = (0, 0, 640, 480)
        self.annotate_text = ""


class FakeOverlay:
    """Mimic the old PiCamera overlay object."""
    def __init__(self, image):
        self.image = image
        self.layer = 0
        self.alpha = 255
        self.fullscreen = True
        self.window = (0, 0, image.shape[1], image.shape[0])


class Camera:
    '''
    Thin wrapper around Picamera2 to mimic old PiCamera API
    Compatible with Pi Camera Module 3 on Raspberry Pi OS Bullseye+
    '''

    def __init__(self):
        self.picam2 = Picamera2()
        config = self.picam2.create_still_configuration(main={"size": (1600, 1200)})
        self.picam2.configure(config)
        self.picam2.start()
        time.sleep(0.5)

        self.preview = DummyPreview()
        self.previewing = False
        self._last_overlay = None

    def start_preview(self):
        self.previewing = True

    def stop_preview(self):
        self.previewing = False

    def capture(self, filename, resize=None):
        """Capture a still image and save to file."""
        frame = self.picam2.capture_array()

        # If overlay exists, ignore for now (no blending yet)
        if isinstance(self._last_overlay, FakeOverlay):
            pass

        cv2.imwrite(filename, frame)

    def close(self):
        self.picam2.stop()

    # ---- Compatibility stubs ----
    def add_overlay(self, image_bytes, size=(640, 480), **kwargs):
        w, h = size
        overlay = np.frombuffer(image_bytes, dtype=np.uint8).reshape((h, w, -1))
        fake = FakeOverlay(overlay)
        self._last_overlay = fake
        return fake

    def remove_overlay(self, overlay):
        self._last_overlay = None


# Alias to mimic picamera import
PiCamera = Camera


def test():
    """Standalone test: live preview with 'q' to quit."""
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
    
