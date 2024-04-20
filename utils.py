def encode_with_newline(input_string):
    if input_string[:4] == "move":
        input_string = input_string.replace(" ", '')
    return f"{input_string}\n".encode()

def prettify_decorator(function):
    def wrapper(*args: any, **kwargs: any): # x for self
        print(f"====={function.__name__}=====")
        function(*args, **kwargs)
        print()
    return wrapper

def extract_coords(coords):
    coords = coords.split("]")[0]
    coords = coords.replace("[", "").replace("]", "").split(",")
    if "" in coords:
        return False
    coords = [int(i) for i in coords]
    return coords