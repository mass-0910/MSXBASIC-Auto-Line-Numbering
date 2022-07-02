import sys
import os
import argparse
from typing import List
import re

label_pat = re.compile(r"(@[A-Za-z][\w0-9]*)")


class AddLineNumberError(Exception):
    pass


class TagError(Exception):
    pass


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="A script that automatically assigns line numbers to BASIC programs")
    parser.add_argument("BASIC_FILE_PATH", help="Path to .bas file")
    parser.add_argument("DEST_FILE_PATH", help="Path to dest file")
    parser.add_argument("-U", "--uppercase", action="store_true", help="Convert to Uppercase")
    args = parser.parse_args()
    return args


def add_line_num(file_buf: List[str], step: int = 10) -> List[str]:
    ln = step
    new_file_buf = []
    for l in file_buf:
        if label_pat.fullmatch(l):
            new_file_buf.append(l)
            continue
        m = re.fullmatch(r"([0-9]+)\s+.+", l)
        if m:
            current_ln = int(m.group(1))
            if current_ln <= ln:
                raise AddLineNumberError("There is a reversion of the number of lines")
            ln = current_ln + step
            new_file_buf.append(l)
        else:
            new_file_buf.append(f"{ln} {l}")
            ln += step
    return new_file_buf


def resolve_tag(file_buf: List[str]) -> List[str]:
    new_file_buf = []
    tag_def = {}
    tag_removed_buf: List[str] = []
    for i, l in enumerate(file_buf):
        m = label_pat.fullmatch(l)
        if m:
            tag_def[m.group(1)] = re.fullmatch(r"([0-9]+)\s+.+", file_buf[i + 1]).group(1)
        else:
            tag_removed_buf.append(l)
    for l in tag_removed_buf:
        m = label_pat.search(l)
        if m:
            if not m.group(1) in tag_def.keys():
                raise TagError(f"{m.group(1)} not defined")
            l = l.replace(m.group(1), tag_def[m.group(1)])
        new_file_buf.append(l)
    return new_file_buf


def uppercase(file_buf: List[str]) -> List[str]:
    new_file_buf = []
    for l in file_buf:
        m = re.fullmatch(r"([0-9]*\s*)(.*)", l)
        if re.fullmatch(r"(?:rem|REM|').*", m.group(2)):
            new_file_buf.append(m.group(1) + re.sub("^rem", "REM", m.group(2)))
            continue
        new_line = ""
        in_literal = False
        for c in l:
            if not in_literal:
                if c == "\"":
                    in_literal = True
                new_line += c.upper()
            else:
                if c == "\"":
                    in_literal = False
                new_line += c
        new_file_buf.append(new_line)
    return new_file_buf


def input_basic(filepath: str) -> List[str]:
    with open(filepath) as fp:
        file_buf = [l.strip() for l in fp.readlines() if not re.fullmatch("\s*", l)]
    return file_buf


def output_basic(filepath: str, file_buf: List[str]):
    with open(filepath, mode='w') as fp:
        for i, l in enumerate(file_buf):
            if i == len(file_buf) - 1:
                fp.write(l)
            else:
                fp.write(l + "\n")


if __name__ == "__main__":
    args = arguments()
    file_buf = input_basic(args.BASIC_FILE_PATH)
    file_buf = add_line_num(file_buf)
    file_buf = resolve_tag(file_buf)
    if args.uppercase:
        file_buf = uppercase(file_buf)
    output_basic(args.DEST_FILE_PATH, file_buf)
