import item


def get_crop(img, box):
    x1, y1, x2, y2 = box
    crop = img[int(y1) : int(y2), int(x1) : int(x2)]
    return crop


def from_img2(model, img, **ignored):
    results = model(img)[0]
    extractions = []
    for detection in results.boxes:
        prediction = model.names[int(detection.cls)]
        crop = get_crop(results.orig_img, detection.xyxy[0])
        extractions.append(item.factory.create(prediction, crop=crop, **ignored))
    return extractions


# YOLOv5 functionality
def from_img(model, img, **ignored):
    detections = model(img).crop(save=False)
    extractions = []
    for crop in detections:
        extractions.append(from_detection(crop, **ignored))
    return extractions


def from_detection(crop, **ignored):
    prediction, _ = crop["label"].split()  # old/yellow/black
    return item.factory.create(prediction, crop=crop["im"], **ignored)
