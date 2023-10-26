import pytesseract
import cv2
import numpy as np

from .rotation import horizontalize, rotate


def mask_img(thresh, cnt):
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


def process_black_label_good(img, kernel):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    invert = cv2.bitwise_not(gray)
    blur = cv2.GaussianBlur(gray, kernel, 0)
    _, thresh = cv2.threshold(blur, 160, 255, cv2.THRESH_BINARY_INV)
    _, rotation_image = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
    ### adaptive ?
    # invert = cv2.bitwise_not(gray)
    # rotation_image = cv2.adaptiveThreshold(
    #   invert, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 10
    # )
    ###
    # rotation_image = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    _, text_img = cv2.threshold(gray, 175, 255, cv2.THRESH_BINARY_INV)
    return thresh, rotation_image, text_img


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


def clean_image(img, kernel):
    invert = cv2.bitwise_not(img)
    opening = cv2.morphologyEx(invert, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    return cv2.bitwise_not(closing)


def process_label(cropped, label_type):
    rotated = horizontalize(cropped)
    shape = rotated.shape[0:2]
    kernel_size = (3, 3)
    if label_type == "black":
        thresh, rotation_image, t_img = process_black_label(rotated, kernel_size)
    else:
        return None, None, None

    # get larges contour
    cnts, _ = cv2.findContours(rotation_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    cnt = cnts[0]

    out = mask_img(thresh, cnt)
    t_img = mask_img(t_img, cnt)

    angle = get_label_rotation(cnt, shape)

    out = rotate(out, angle)
    t_img = rotate(t_img, angle)
    # out = clean_image(out, kernel)

    return out, rotation_image, t_img


def extract_text(img, conf=0.6):
    df = pytesseract.image_to_data(
        img,
        lang="dan",
        output_type="data.frame",
        config="--psm 1 --user-patterns text_patterns.patterns",  # TODO configure pytesseract to search some custom words?
    )
    df = df[df.conf > conf]
    words = df.text.tolist()
    text = " ".join([str(word) for word in words])
    return text


def process_label2(cropped):
    rotated = horizontalize(cropped)
    shape = rotated.shape[0:2]
    kernel_size = (1, 1)  ## change depending on resolution?
    invert, rotation_image, t_img = process_black_label(rotated, kernel_size)

    # get larges contour
    cnts, _ = cv2.findContours(rotation_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    cnt = cnts[0]

    out = mask_img(invert, cnt)
    t_img = mask_img(t_img, cnt)

    angle = get_label_rotation(cnt, shape)

    out = rotate(out, angle)
    t_img = rotate(t_img, angle)
    # out = clean_image(out, kernel)

    return out, t_img, out


def get_label_contour(img):
    # we assume the largest contour on the img is the label.
    cnts, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    return cnts[0]


def process(crop):
    horizontal = horizontalize(crop)
    invert = get_invert(horizontal)
    _, thresh = cv2.threshold(invert, 175, 255, cv2.THRESH_BINARY)
    contour = get_label_contour(thresh)

    out = mask_img(invert, contour)
    angle = get_label_rotation(contour, horizontal.shape[0:2])
    out = rotate(out, angle)
    return out


def get_invert(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    invert = cv2.bitwise_not(gray)
    return invert


def process_black_label(img, kernel):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    invert = cv2.bitwise_not(gray)
    blur = cv2.GaussianBlur(gray, kernel, 0)
    _, thresh = cv2.threshold(blur, 160, 255, cv2.THRESH_BINARY_INV)
    _, rotation_image = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
    ### adaptive ?
    # invert = cv2.bitwise_not(gray)
    # rotation_image = cv2.adaptiveThreshold(
    #   invert, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 10
    # )
    ###
    # rotation_image = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    _, text_img = cv2.threshold(gray, 175, 255, cv2.THRESH_BINARY_INV)
    return invert, rotation_image, text_img
