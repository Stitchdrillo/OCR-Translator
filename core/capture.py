from PIL import ImageGrab
def capture_region(x, y, width, height):
    left = x
    top = y
    right = x + width
    bottom = y + height
    bbox = (left, top, right, bottom)
    image = ImageGrab.grab(bbox)
    return image
