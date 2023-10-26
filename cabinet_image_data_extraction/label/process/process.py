import cv2
import numpy as np

from .rotation import horizontalize, rotate, get_label_rotation


def upscale_image(input_path, output_path, scale_factor):
    # Open the image file
    img = Image.open(input_path)

    # Get the original dimensions
    original_width, original_height = img.size

    # Calculate the new dimensions after upscaling
    new_width = int(original_width * scale_factor)
    new_height = int(original_height * scale_factor)

    # Perform the upscaling
    upscaled_img = img.resize((new_width, new_height), Image.LANCZOS)

    # Save the upscaled image
    upscaled_img.save(output_path)


def mask_img(thresh, cnt, val=255):
    mask = np.zeros_like(
        thresh
    )  # Create mask where white is what we want, black otherwise
    cv2.drawContours(mask, [cnt], 0, 255, -1)  # Draw filled contour in mask
    out = np.ones_like(thresh) * 255
    # Extract out the object and place into output image
    out[mask == 255] = thresh[mask == 255]
    (y, x) = np.where(mask == 255)[0:2]
    (topy, topx) = (np.min(y), np.min(x))
    (bottomy, bottomx) = (np.max(y), np.max(x))
    out = out[topy : bottomy + 1, topx : bottomx + 1]
    return out


def get_label_contour(img):
    # we assume the largest contour on the img is the label.
    cnts, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    return cnts[0]


def get_invert(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    invert = cv2.bitwise_not(gray)
    return invert


def process(crop):
    horizontal = horizontalize(crop)
    invert = get_invert(horizontal)
    _, countour_img = cv2.threshold(invert, 150, 255, cv2.THRESH_BINARY)
    contour = get_label_contour(countour_img)

    out = mask_img(invert, contour)
    angle = get_label_rotation(contour, horizontal.shape[0:2])
    out = rotate(out, angle)
    # median = cv2.medianBlur(out, 5)
    out[out > 125] = 255
    return out


def process2(crop):
    horizontal = horizontalize(crop)
    gray = cv2.cvtColor(horizontal, cv2.COLOR_BGR2GRAY)
    # for getting countour
    invert = get_invert(horizontal)
    _, countour_img = cv2.threshold(invert, 150, 255, cv2.THRESH_BINARY)
    contour = get_label_contour(countour_img)

    masked = mask_img(gray, contour, val=0)
    angle = get_label_rotation(contour, horizontal.shape[0:2])
    rectified = rotate(masked, angle)
    _, thresh = cv2.threshold(rectified, 150, 255, cv2.THRESH_TOZERO)

    return thresh
