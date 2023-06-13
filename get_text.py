import pytesseract
import cv2
import numpy as np


def rotate_image(image, angle):
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


def process_black_label(img, kernel):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thresh = cv2.threshold(blur, 160, 255, cv2.THRESH_BINARY_INV)
    # thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 10)
    _, rotation_image = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
    _, text_img = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    return thresh, rotation_image, text_img


def get_label_rotation(cnt, shape):
    rows, cols = shape
    [vx, vy, x, y] = cv2.fitLine(cnt, cv2.DIST_L2, 0, 0.01, 0.01)
    x_axis = np.array([1, 0])  # unit vector in the same direction as the x axis
    your_line = np.array([vx, vy])  # unit vector in the same direction as your line
    dot_product = np.dot(x_axis, your_line)
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


def check_rotation(img):
    try:
        h, w = img.shape
    except ValueError:
        h, w, dim = img.shape
    if w < h:
        rotated = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return rotated
    return img


def process_label(cropped, label_type):
    rotated = check_rotation(cropped)
    shape = rotated.shape[0:2]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    if label_type == "black":
        thresh, rotation_image, t_img = process_black_label(rotated, kernel)
    else:
        return None, None, None

    # get larges contour
    cnts, _ = cv2.findContours(rotation_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    cnt = cnts[0]

    out = mask_img(thresh, cnt)
    angle = get_label_rotation(cnt, shape)
    out = rotate_image(out, angle)
    # out = clean_image(out, kernel)

    return out, rotation_image, t_img


def extract_text(img, conf=0.85):
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
