import pytesseract


# MATCH STÆRKNINGSKILT VIL ALTID VÆRE SAMME TRANSFOERM STATION SOM DEN FØR, match med: -nummer??
def extract_df(img, conf=0.85, psm=3):
    config = f"--psm {psm}"
    # config = "load_system_dawg=0 load_freq_dawg=0 user_patterns_suffix=text_patterns.patterns"
    df = pytesseract.image_to_data(
        img,
        lang="dan",
        output_type="data.frame",
        config=config,  # TODO configure pytesseract to search some custom words?
    )
    # before was psm 1
    df = df[df.conf > conf]
    return df


def df_to_str(df):
    words = df.text.tolist()
    text = " ".join([str(word) for word in words])
    return text


def extract(img, conf=0.6, psm=3):  # 0.6
    config = f"--psm {psm}"
    # config = "load_system_dawg=0 load_freq_dawg=0 user_patterns_suffix=text_patterns.patterns"
    df = pytesseract.image_to_data(
        img,
        lang="dan",
        output_type="data.frame",
        config=config,  # TODO configure pytesseract to search some custom words?
    )
    # before was psm 1
    df = df[df.conf > conf]
    words = df.text.tolist()
    text = " ".join([str(word) for word in words])
    return text
