import pytesseract


def extract_text(img, conf=0.6):
    df = pytesseract.image_to_data(
        img,
        lang="dan",
        output_type="data.frame",
        config="--psm 1 --user-patterns text_patterns.patterns --oem 3 -c tessedit_char_whitelist=0123456789",  # TODO configure pytesseract to search some custom words?
    )
    df = df[df.conf > conf]
    words = df.text.tolist()
    text = " ".join([str(word) for word in words])
    return text
