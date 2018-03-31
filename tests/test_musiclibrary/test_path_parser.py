import pytest
from discogs_search.musiclibrary.scanner import Scanner

@pytest.fixture(scope='module')
def parse_result():
    return {'year': '1990', 'artist': 'Kyuss', 'album': 'Sons of Kyuss'}



def create_scanner(pattern):
    return Scanner('somefolder', pattern)


def test__pasre_path_my_pattern(parse_result):
    pattern = '%A/%Y - %a'
    sc = create_scanner(pattern)

    # windows path
    path = 'C:\\mymusic\\Kyuss\\1990 - Sons of Kyuss'
    assert sc._parse_path(path) == parse_result
    # *nix path
    path = '/mymusic/Kyuss/1990 - Sons of Kyuss'
    assert sc._parse_path(path) == parse_result


def test__pasre_path_another_pattern(parse_result):
    pattern = '%A/%Y/%a'
    sc = create_scanner(pattern)

    # windows path
    path = 'C:\\mymusic\\Kyuss\\1990\\Sons of Kyuss'
    assert sc._parse_path(path) == parse_result
    # *nix path
    path = '/mymusic/Kyuss/1990/Sons of Kyuss'
    assert sc._parse_path(path) == parse_result


def test__pasre_path_parentheses_pattern(parse_result):
    pattern = '%A/%a (%Y)'
    sc = create_scanner(pattern)

    # windows path
    path = 'C:\\mymusic\\Kyuss\\Sons of Kyuss (1990)'
    assert sc._parse_path(path) == parse_result
    # *nix path
    path = '/mymusic/Kyuss/Sons of Kyuss (1990)'
    assert sc._parse_path(path) == parse_result


def test__pasre_path_parentheses_pattern2(parse_result):
    pattern = '%A/(%Y) %a'
    sc = create_scanner(pattern)

    path = 'C:\\mymusic\\Kyuss\\(1990) Sons of Kyuss'
    # windows path
    assert sc._parse_path(path) == parse_result
    # *nix path
    path = '/mymusic/Kyuss/(1990) Sons of Kyuss'
    assert sc._parse_path(path) == parse_result


def test__pasre_path_square_parentheses_pattern(parse_result):
    pattern = '%A/%a [%Y]'
    sc = create_scanner(pattern)

    # windows path
    path = 'C:\\mymusic\\Kyuss\\Sons of Kyuss [1990]'
    assert sc._parse_path(path) == parse_result
    # *nix path
    path = '/mymusic/Kyuss/Sons of Kyuss [1990]'
    assert sc._parse_path(path) == parse_result


def test__pasre_path_figure_parentheses_at_the_end(parse_result):
    pattern = '%A/%a {%Y}'
    sc = create_scanner(pattern)

    # windows path
    path = 'C:\\mymusic\\Kyuss\\Sons of Kyuss {1990}'
    assert sc._parse_path(path) == parse_result

def test__pasre_path_figure_parentheses_at_the_beginning(parse_result):
    pattern = '%A/{%Y} %a'
    sc = create_scanner(pattern)

    # *nix path
    path = '/mymusic/Kyuss/{1990} Sons of Kyuss'
    assert sc._parse_path(path) == parse_result


def test__parse_path_no_year(parse_result):
    pattern = '%A/%a'
    sc = create_scanner(pattern)
    parse_result.pop('year')

    # windows path
    path = 'C:\\mymusic\\Kyuss\\Sons of Kyuss'
    assert sc._parse_path(path) == parse_result

    # *nix path
    path = '/mymusic/Kyuss/Sons of Kyuss'
    assert sc._parse_path(path) == parse_result


def test__parse_path_digits_in_names():
    pattern = '%A/%Y - %a'
    sc = create_scanner(pattern)

    # windows path
    path = 'C:\\some\\deep\\folder\\20-20s\\1990 - Sons of Kyuss'
    assert sc._parse_path(path) == {'artist': '20-20s', 'year': '1990', 'album':'Sons of Kyuss'}


def test__parse_path_symbols_in_names():
    pattern = '%A/%Y - %a'
    sc = create_scanner(pattern)

    # windows path
    path = 'C:\\some\\deep\\folder\\20-(20\'s)\\1990 - Sons + Kyuss'
    assert sc._parse_path(path) == {'artist': '20-(20\'s)', 'year': '1990', 'album':'Sons + Kyuss'}
