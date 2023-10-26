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
    R = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(
        image,
        R,
        image.shape[1::-1],
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=255,
    )
    return result


def get_label_rotation(cnt, shape):
    rows, cols = shape
    [vx, vy, x, y] = cv2.fitLine(cnt, cv2.DIST_L2, 0, 0.01, 0.01)
    x_axis = np.array([1, 0])  # unit vector in the same direction as the x axis
    line = np.array([vx, vy])  # unit vector in the same direction as our line
    dot_product = np.dot(x_axis, line)
    angle_2_x = np.degrees(np.arccos(dot_product))
    angle_2_x = float(angle_2_x)
    if vy < 0:
        angle_2_x = -angle_2_x

    return angle_2_x
