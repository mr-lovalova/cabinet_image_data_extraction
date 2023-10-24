import objects


def from_img(model, img):
    detections = model(img).crop(save=False)
    extractions = []
    for crop in detections:
        extracted = from_detection(crop)
        if extracted:
            extractions.append(extracted)
    return extractions


def from_detection(crop):
    prediction, _ = crop["label"].split()  # old/yellow/black
    if prediction != "black":  # temp until new model without y/b
        return None
    return objects.factory.create(prediction, image=crop["im"])
