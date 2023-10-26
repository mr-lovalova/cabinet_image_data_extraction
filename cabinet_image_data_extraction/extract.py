import objects


def from_img(model, img, log):
    detections = model(img).crop(save=False)
    extractions = []
    for crop in detections:
        extracted = from_detection(crop, log)
        if extracted:
            extractions.append(extracted)
    return extractions


def from_detection(crop, log):
    prediction, _ = crop["label"].split()  # old/yellow/black
    if prediction != "black":  # temp until new model without y/b
        return None
    return objects.factory.create(prediction, image=crop["im"], log=log)
