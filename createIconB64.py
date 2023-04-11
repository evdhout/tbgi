import base64
from pathlib import Path

if __name__ == "__main__":
    icon_filename = "resources/icon.png"
    icon_path = Path(icon_filename)

    if not icon_path.is_file():
        print(f"{icon_filename} does not exist")
        exit(1)

    icon_py_filename = "views/icon.py"
    icon_py_path = Path(icon_py_filename)

    if icon_py_path.is_file():
        replace = input(f"{icon_py_filename} exists, overwrite (y/N)? ")
        if replace.lower() not in ["y", "yes", "j", "ja"]:
            print(f"Not replacing {icon_py_filename}.")
            exit()

    icon_file = open(icon_path, "rb")
    icon_data = icon_file.read()
    icon_b64 = base64.b64encode(icon_data)

    icon_py_file = open(icon_py_path, "w+")
    icon_py_file.write(f'b64icon={icon_b64}\n')
    icon_py_file.close()

    print(f"Generated {icon_py_filename} with b64 representation of {icon_filename}")
