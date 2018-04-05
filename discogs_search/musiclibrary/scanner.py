import os
import re
import logging
from pathlib import Path


logger = logging.getLogger('Scanner')


class Scanner:
    class ParsePathError(Exception):
        def __init__(self, path):
            self.msg =  'Can\'t parse "{}"'.format(path)

        def __repr__(self):
            return '{}: {}'.format('ParsePathError', self.msg)


    def __init__(self, folder, pattern):
        self.folder = folder
        self._path_regex = self._prepare_regex(pattern)

    def _prepare_regex(self, pattern):
        """Replacing user pattern with regex patterns a compile it

        :param pattern: user pattern for path
        :type pattern: str
        :return: compiled regex pattern
        """
        # escaping all characters
        pattern = re.escape(pattern)
        replacers = [(r'\\/', r'[\\\\/]'),
                     (r'\\%A', r'(?P<artist>[\w\'.\-\+() ]+)'),
                     (r'\\%Y', r'(?P<year>\d\d\d\d)'),
                     (r'\\%a', r'(?P<album>[\w\'.\-\+() ]+)')]
        # replacing user pattern with re patterns
        for subpattern, replacer in replacers:
            pattern = re.sub(subpattern, replacer, pattern)
        pattern += '$'
        return re.compile(pattern)


    def _parse_path(self, path):
        result = self._path_regex.search(path)
        if result:
            return result.groupdict()
        else:
            raise self.ParsePathError(path)

    def scan(self):
        """
        Scan folder for structure given in patten.

        :Example:

        >>> for album_data in Scanner('home/music', '%A/%a (%Y)').scan():
        ...     print(album_data)
        {'year': '1990', 'artist': 'Kyuss', 'album': 'Sons of Kyuss'}
        {'year': '1990', 'artist': 'Kyuss', 'album': 'Sons of Kyuss'}
        ...

        :return: yields dicts with artist, year and album
        :rtype: Iterator[dict]
        """
        for root, _, _ in os.walk(self.folder):
           try:
               yield self._parse_path(root)
           except self.ParsePathError:
               logger.info('Can\'t parse "$s"', root)






