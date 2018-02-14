import os
import re
from pathlib import Path


def _isformat(filename, formats):
    """Compares file to file format"""
    for format_ in formats:
        if Path(filename).suffix.lower() == '.{}'.format(format_):
            return True
    return False


def scan(folder, formats):
    """Scan folder and return files that are in given format.

    :param folder: Path to folder
    :type folder: str
    :param formats: file formats to find
    :type formats: list
    :return: list of tuples ``[(folder_path, filename,) ...]``
    :rtype: list
    """
    files_found = []
    for root, _, files in os.walk(folder):
        files_found.extend([(root, file) for file in files if _isformat(file, formats)])
    return files_found


def _parse_path(path, pattern):
    # escaping all characters
    pattern = re.escape(pattern)
    replacers = [(r'\\/', r'[\\\\/]'),
                 (r'\\%A', r'(?P<artist>[\w ]+)'),
                 (r'\\%Y', r'(?P<year>\d\d\d\d)'),
                 (r'\\%a', r'(?P<album>[\w ]+)')]
    # replacing pattern with re patterns
    for p, repl in replacers:
        pattern = re.sub(p, repl, pattern)
    pattern += '$'
    result = re.search(pattern, path)
    if result:
        return result.groupdict()
    else:
        return None



