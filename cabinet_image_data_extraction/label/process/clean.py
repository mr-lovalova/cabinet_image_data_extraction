import cv2
import numpy as np
from .rotation import horizontalize, rotate, get_text_angle


def is_blurry(img, threshold):
    variance = cv2.Laplacian(img, cv2.CV_64F).var()
    print(variance)
    return threshold > variance


def mask_img(img, cnt):
    mask = np.zeros_like(
        img
    )  # Create mask where white is what we want, black otherwise
    cv2.drawContours(mask, [cnt], 0, 255, -1)  # Draw filled contour in mask
    out = np.ones_like(img) * 255
    # Extract out the object and place into output image
    out[mask == 255] = img[mask == 255]
    return out


def calculate_brightness(gray):
    # Calculate the average pixel intensity
    brightness = int(gray.mean())
    return brightness


def get_label_contour(img, threshhold):
    # we assume the largest contour on the countour_img is the label.
    _, countour_img = cv2.threshold(img, threshhold, 255, cv2.THRESH_BINARY)
    cnts, _ = cv2.findContours(countour_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    try:
        return cnts[0]
    except IndexError:
        threshhold -= 5
        contour = get_label_contour(img, threshhold)
        if threshhold < 50:
            return None


def get_invert(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    invert = cv2.bitwise_not(gray)
    return invert


def normalize(img):
    normalized = cv2.normalize(img, None, 0, 1, cv2.NORM_MINMAX)
    return normalized


def sharpen(gray):
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened = cv2.filter2D(blurred, -1, kernel)
    return sharpened


def process(crop):
    horizontal = horizontalize(crop)
    invert = get_invert(horizontal)

    contour = get_label_contour(invert, 150)
    brighness = calculate_brightness(invert)

    if contour is not None:
        out = mask_img(invert, contour)
    else:
        out = invert
    out[out > 125] = 200
    out = rotate(out, get_text_angle(out))
    out = cv2.dilate(out, (3, 3), iterations=1)
    # out = add_border(out)
    return out


def add_border(img, size=10):
    height, width = img.shape
    image_with_border = np.ones((height, width + size), dtype=np.uint8) * 255
    image_with_border[:, size : size + width] = img  # leftside border
    return image_with_border
