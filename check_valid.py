invalid_char = r'<>:"/\|?* '

def overwrite_invalid(filename):
    for char in invalid_char:
        filename = filename.replace(char, "_")
    return filename
