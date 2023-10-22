import numpy as np
import cv2


def horizontalize(img):
    """returns a horizontally oriented label. (possibly upside down if image is upside down)"""
    try:
        h, w = img.shape
    except ValueError:
        h, w, dim = img.shape
    if w < h:
        rotated = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return rotated
    return img


def rotate(image, angle):
    """rotates image by an angle"""
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(
        image,
        rot_mat,
        image.shape[1::-1],
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=255,
    )
    return result
