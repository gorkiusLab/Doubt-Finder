"""
  __ \                 |      |        ____| _)             |
  |   |   _ \   |   |  __ \   __|      |      |  __ \    _` |   _ \   __|
  |   |  (   |  |   |  |   |  |        __|    |  |   |  (   |   __/  |
 ____/  \___/  \__,_| _.__/  \__|     _|     _| _|  _| \__,_| \___| _|
A simple CLI program that looks for a doubt sequence in a given directories files and subdirectories

Supported file types -> txt, odt and docx
Alpha 1.0

Copyright (c) 2023 - Public Domain
The author(s) of this work hereby waive all copyright and related or neighboring rights to this work, to the extent
possible under law. This work is published from: Spain, Basque Country.

title font 'shadow' by Glenn Chappell found in https://ascii.today.

used packages:
docx - Copyright (c) 2013 Steve Canny, https://github.com/scanny.
odfpy - Copyright (C) 2006-2014, Daniel Carrera, Alex Hudson, Søren Roug, Thomas Zander, Roman Fordinal, Michael Howitz
and Georges Khaznadar https://github.com/eea/odfpy.

By gorkius
"""

import os
import docx
from odf import opendocument, text

show_errors = (False, True)
DEFAULT_DOUBT_SEQUENCE = '(?)'
text_style = {
    "purple": '\033[95m',
    "sky": '\033[94m',
    "cyan": '\033[96m',
    "green": '\033[92m',
    "yellow": '\033[93m',
    "red": '\033[91m',
    "white": '\033[0m',
    "bold": '\033[1m',
    "underline": '\033[4m'
}

directory: str


def _blank_line():
    print()


def _press_enter():
    input(f"{text_style['cyan']}Press enter to quit...")


def _set_directory():
    global directory
    while True:
        directory = input(f"{text_style['white']}Enter the directory: ")
        if os.path.isdir(directory):
            break
        print(f"{text_style['red']}The given directory is wrong!")


def _get_extension(file):
    return file[file.rfind('.') + 1:]


def _is_compatible_file(file):
    extension = _get_extension(file)
    return extension == 'txt' or extension == 'odt' or extension == 'docx'


def _get_relative_path(from_, to):
    relative_path = to.replace(from_, "")
    return relative_path if relative_path else "the base directory"


def _show_error(exc):
    return (show_errors[0] and show_errors[1]) or \
        (isinstance(exc, UnicodeDecodeError) and show_errors[0]) or \
        (isinstance(exc, PermissionError) and show_errors[1])


def _check_for_doubt(file, file_dir):
    extension = _get_extension(file)
    if extension == 'txt':
        try:
            with open(os.path.join(file_dir, file), 'r', encoding="utf-8") as f:
                for idx_line, line in enumerate(f):
                    if DEFAULT_DOUBT_SEQUENCE in line:
                        print(f"{text_style['yellow']}Found doubt at line {idx_line + 1} in file {file} in "
                              f"{_get_relative_path(directory, file_dir)}.")
        except (UnicodeDecodeError, PermissionError) as exc:
            if _show_error(exc):
                print(f"{text_style['red']}Error while reading file {file} in "
                      f"{_get_relative_path(directory, file_dir)}")
                print(exc)

    elif extension == 'odt':
        doc = opendocument.load(os.path.join(file_dir, file))
        lines = doc.getElementsByType(text.P)
        for idx_line, line in enumerate(lines):
            if DEFAULT_DOUBT_SEQUENCE in str(line):
                print(f"{text_style['yellow']}Found doubt at line {idx_line + 1} in file {file} in "
                      f"{_get_relative_path(directory, file_dir)}.")

    elif extension == 'docx':
        doc = docx.Document(os.path.join(file_dir, file))
        lines = doc.paragraphs
        for idx_line, line in enumerate(lines):
            if DEFAULT_DOUBT_SEQUENCE in line.text:
                print(f"{text_style['yellow']}Found doubt at line {idx_line + 1} in file {file} in "
                      f"{_get_relative_path(directory, file_dir)}.")


def main():
    _set_directory()
    _blank_line()
    # loop through the directory
    for dirpath, _, filenames in os.walk(directory):
        # loop through files in filenames
        for file in filenames:
            if not _is_compatible_file(file):
                continue
            _check_for_doubt(file, dirpath)
    _blank_line()
    _press_enter()


if __name__ == '__main__':
    main()
