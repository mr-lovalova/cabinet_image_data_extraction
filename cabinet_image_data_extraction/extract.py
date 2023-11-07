import factories


def from_img(model, img, **ignored):
    detections = model(img).crop(save=False)
    extractions = []
    for crop in detections:
        extracted = from_detection(crop, **ignored)
        if extracted:
            extractions.append(extracted)
    return extractions


def from_detection(crop, **ignored):
    prediction, _ = crop["label"].split()  # old/yellow/black
    if prediction != "black":  # temp until new model without y/b
        return None
    return factories.item.create(prediction, image=crop["im"], **ignored)
