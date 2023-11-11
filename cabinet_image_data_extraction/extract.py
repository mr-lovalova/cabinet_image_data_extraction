import factories


def from_img(model, img, **ignored):
    detections = model(img).crop(save=False)
    extractions = []
    for crop in detections:
        extractions.append(from_detection(crop, **ignored))
    return extractions


def from_detection(crop, **ignored):
    prediction, _ = crop["label"].split()  # old/yellow/black
    return factories.item.create(prediction, crop=crop["im"], **ignored)
