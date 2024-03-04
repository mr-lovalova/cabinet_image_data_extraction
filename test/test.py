import sys
import json
import pandas as pd
import ast

sys.path.append(".")

from config import RESULTS_FILE_PATH, TEST_DATA_PATH

RESULTS = RESULTS_FILE_PATH
PATH = TEST_DATA_PATH


def lookup_box(df, id_):
    result = lookup_value(df, "id", id_)
    return result


def lookup_value(df, key, value):
    result = df[df[key] == value]
    return result


def start_empty_results_file(file_path):
    with open(file_path, "w"):
        pass


def get_connections(match_df, type_):
    connections = set(ast.literal_eval(match_df[type_].values[0]))
    return connections


def get_box_connections(df, id_, *types):
    match_ = lookup_box(df, id_)
    if match_.empty:
        print(f"Possibly missing cabinet box in db with id: {id_}")
        return None
    connections = [get_connections(match_, type_) for type_ in types]
    return connections


def id_in_box(df, search_id_, box_id, type_):
    connections = get_box_connections(df, box_id, type_)
    if not connections or search_id_ not in connections[0]:
        return False
    return True


def get_labels(box, format):
    labels = set()
    for label in box["labels"]:
        if label["format"] == format:
            labels.add(label["id"])
    return labels


def build_testset(path="testset.txt"):
    with open(path, "r") as file:
        lines = file.readlines()

    testset = {}
    for line in lines:
        print(line)
        entry_dict = json.loads(line)
        entry_id = entry_dict.pop("id")
        testset[entry_id] = entry_dict

    return testset


def validate(box_id, new_item_ids, testset):
    dct = testset.get(box_id, None)
    results = {}
    if not dct:
        results["new"] = new_item_ids
        return results
    # for item_id in new_item_ids:


def generate_output(box, found_labels, known_labels, testset):
    box_id = box["id"]
    matched = list(known_labels & found_labels)
    unmatched = list(found_labels - known_labels)
    out = {"ID": box_id, "INTERSECTION": matched}
    for label in unmatched:
        if label == box_id:
            continue
        validated = validate_item(box_id, label, testset)
        if validated not in out:
            out[validated] = []
        out[validated].append(label)

    return out


def validate_item(box_id, item_id, testset):
    dct = testset.get(box_id, None)
    print("DICT", dct)
    if not dct:
        return "NEW"
    is_wrong = item_id in dct["wrong"]
    is_verified = item_id in dct["verified"]
    if is_wrong and is_verified:
        raise SyntaxError()
    elif is_wrong:
        return "FALSE_POSITIVE"
    elif is_verified:
        return "TRUE_POSITIVE"
    elif not is_wrong and not is_verified:
        return "NEW"


def main():
    testset = build_testset()
    totally_new = set()
    intersection = set()
    correctly_found = set()
    wrongly_found = set()
    db = set()
    found = set()
    not_found = set()
    df = pd.read_csv(PATH)
    FILE = "test.txt"
    start_empty_results_file(FILE)

    with open(RESULTS, "r") as f:
        lines = f.readlines()

    for _, line in enumerate(lines):
        box = json.loads(line)
        print(box)
        tso_labels = get_labels(box, "CONNECTION_POINT")
        cabinet_labels = get_labels(box, "SUBSECTION")
        id_ = box["id"]
        connections = get_box_connections(df, id_, "TSO", "CABINETS")
        if not connections:
            continue
        tso_db, cabinet_db = connections

        for cabinet_id in cabinet_labels:
            if id_in_box(df, id_, cabinet_id, "CABINETS"):
                cabinet_db.add(cabinet_id)

        found_labels = tso_labels.union(cabinet_labels)
        known_labels = tso_db.union(cabinet_db)

        out = generate_output(box, found_labels, known_labels, testset)

        correctly_found = correctly_found.union(out.get("INTERSECTION", set())).union(
            out.get("TRUE_POSITIVE", set())
        )
        wrongly_found = wrongly_found.union(out.get("FALSE_POSITIVE", set()))
        totally_new = totally_new.union(out.get("NEW", set()))

        intersection.update(known_labels & found_labels)
        not_found.update(known_labels - found_labels)
        found.update(found_labels)

        db.update(known_labels)
        with open(FILE, "a") as f:
            f.write(json.dumps(out) + "\n")

    print("CORRECTLY FOUND", len(correctly_found))
    print("WRONGLY FOUND", len(wrongly_found))
    print("NEW", len(totally_new))
    print(
        "PRECISION", len(correctly_found) / (len(wrongly_found) + len(correctly_found))
    )

    print("INTERSECTION", len(intersection))


if __name__ == "__main__":
    main()
