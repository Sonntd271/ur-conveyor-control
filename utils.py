def encode_with_newline(input_string):
    if input_string[:4] == "move":
        input_string = input_string.replace(" ", '')
    return f"{input_string}\n".encode()

def prettify_decorator(function):
    def wrapper():
        print(f"====={function.__name__}=====")
        print(function())
        print()
    return wrapper

def extract_coords(coords):
    coords = coords.replace("[", "").replace("]", "").split(",")
    if "" in coords:
        return False
    coords = [int(i) for i in coords]
    return coords