from discogs_search.musiclibrary import scanner


def test__pasre_path_my_pattern():
    # windows path
    path = 'C:\\mymusic\\Kyuss\\1990 - Sons of Kyuss'
    pattern = '%A/%Y - %a'
    parse_result = {'year': '1990', 'artist': 'Kyuss', 'album': 'Sons of Kyuss'}
    assert scanner._parse_path(path, pattern) == parse_result
    # *nix path
    path = '/mymusic/Kyuss/1990 - Sons of Kyuss'
    assert scanner._parse_path(path, pattern) == parse_result


def test__pasre_path_another_pattern():
    # windows path
    path = 'C:\\mymusic\\Kyuss\\1990\\Sons of Kyuss'
    pattern = '%A/%Y/%a'
    parse_result = {'year': '1990', 'artist': 'Kyuss', 'album': 'Sons of Kyuss'}
    assert scanner._parse_path(path, pattern) == parse_result
    # *nix path
    path = '/mymusic/Kyuss/1990/Sons of Kyuss'
    assert scanner._parse_path(path, pattern) == parse_result


def test__pasre_path_parentheses_pattern():
    # windows path
    path = 'C:\\mymusic\\Kyuss\\Sons of Kyuss (1990)'
    pattern = '%A/%a (%Y)'
    parse_result = {'year': '1990', 'artist': 'Kyuss', 'album': 'Sons of Kyuss'}
    assert scanner._parse_path(path, pattern) == parse_result
    # *nix path
    path = '/mymusic/Kyuss/Sons of Kyuss (1990)'
    assert scanner._parse_path(path, pattern) == parse_result


def test__pasre_path_parentheses_pattern2():
    # windows path
    path = 'C:\\mymusic\\Kyuss\\(1990) Sons of Kyuss'
    pattern = '%A/(%Y) %a'
    parse_result = {'year': '1990', 'artist': 'Kyuss', 'album': 'Sons of Kyuss'}
    assert scanner._parse_path(path, pattern) == parse_result
    # *nix path
    path = '/mymusic/Kyuss/(1990) Sons of Kyuss'
    assert scanner._parse_path(path, pattern) == parse_result


def test__pasre_path_square_parentheses_pattern():
    # windows path
    path = 'C:\\mymusic\\Kyuss\\Sons of Kyuss [1990]'
    pattern = '%A/%a [%Y]'
    parse_result = {'year': '1990', 'artist': 'Kyuss', 'album': 'Sons of Kyuss'}
    assert scanner._parse_path(path, pattern) == parse_result
    # *nix path
    path = '/mymusic/Kyuss/Sons of Kyuss [1990]'
    assert scanner._parse_path(path, pattern) == parse_result


def test__pasre_path_figure_parentheses_pattern():
    # windows path
    path = 'C:\\mymusic\\Kyuss\\Sons of Kyuss {1990}'
    pattern = '%A/%a {%Y}'
    parse_result = {'year': '1990', 'artist': 'Kyuss', 'album': 'Sons of Kyuss'}
    assert scanner._parse_path(path, pattern) == parse_result
    # *nix path
    path = '/mymusic/Kyuss/{1990} Sons of Kyuss'
    pattern = '%A/{%Y} %a'
    assert scanner._parse_path(path, pattern) == parse_result