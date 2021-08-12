import os
from argparse import ArgumentTypeError


def argparse_file_exists(filename: str) -> str:
    try:
        return file_exists(filename)
    except FileNotFoundError as e:
        raise ArgumentTypeError(e)


def argparse_directory_exists(directory: str) -> str:
    try:
        return directory_exists(directory)
    except NotADirectoryError as e:
        raise ArgumentTypeError(e)


def file_exists(filename: str) -> str:
    if os.path.isfile(os.path.expanduser(filename)):
        return os.path.expanduser(filename)
    else:
        raise FileNotFoundError(f'Bestand "{filename}" bestaat niet.')


def directory_exists(directory: str) -> str:
    if os.path.isdir(os.path.expanduser(directory)):
        return os.path.expanduser(directory)
    else:
        raise NotADirectoryError(f'Directory "{directory}" bestaat niet.')
