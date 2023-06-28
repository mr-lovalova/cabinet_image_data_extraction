def dimension(x):
    count, char = x
    if char.isdigit():
        if count >= 5 and char == str(2):
            return False

    if char == "m" or char.isspace():
        return False

    return True


def ampere(x):
    count, char = x
    if char.isspace():
        return False
    return True


def address(x):
    count, char = x
    return True


filters = {
    "dimension": dimension,
    "ampere": ampere,
    "address": address,
}

maps = {
    "dimension": lambda x: x[1].upper(),
    "ampere": lambda x: x[1].upper(),
    "address": lambda x: x[1],
}
