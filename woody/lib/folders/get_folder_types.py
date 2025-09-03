def get_folder_type(depth):
    if depth == 0:
        return "root"
    elif depth == 1:
        return "group"
    elif depth == 2:
        return "asset"
    else:
        return "type"