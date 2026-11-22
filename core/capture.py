"""Screen region capture utilities."""

from PIL import Image, ImageGrab


def capture_region(x: int, y: int, width: int, height: int) -> Image.Image:
    """Capture a rectangular region of the screen in physical pixel coordinates."""
    bbox = (x, y, x + width, y + height)
    return ImageGrab.grab(bbox=bbox)
