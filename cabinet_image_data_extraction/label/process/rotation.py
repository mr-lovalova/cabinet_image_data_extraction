import numpy as np
import cv2
import pytesseract
from pytesseract import Output


def show(img, title="none"):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def is_possibly_upside_down(img):
    """possebly is important here ^^"""
    try:
        orientation = pytesseract.image_to_osd(img, output_type=Output.DICT)[
            "orientation"
        ]
        if orientation == 180:
            upside_down = True
        else:
            upside_down = False
    except:
        upside_down = False

    return upside_down


def horizontalize(img):
    """returns a horizontally oriented label. (possibly upside down)"""
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
    angle = np.deg2rad(angle)
    result = cv2.warpAffine(
        image,
        R,
        image.shape[1::-1],
        borderValue=200,
    )
    return result


def get_text_angle(img):
    edges = cv2.Sobel(img, cv2.CV_8U, 0, 1, ksize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 20)  # 75 #20

    try:
        horizontal_lines = [
            line
            for line in lines
            if np.abs(np.cos(line[0][1])) < np.abs(np.sin(line[0][1]))
        ]
    except TypeError:
        return 0

    if not horizontal_lines:
        return 0

    best_line = horizontal_lines[0]
    rho, theta = best_line[0]
    angle = np.degrees(theta) - 90
    """    print(angle)
    # for logging images
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))

    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    # Display the result
    cv2.imshow("Detected Lines", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imshow("Detected Lines", rotate(img, angle))
    cv2.waitKey(0)
    cv2.destroyAllWindows()"""

    return angle
