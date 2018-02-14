import shutil
from pathlib import Path
import pytest
from discogs_search.musiclibrary import scanner


@pytest.fixture(scope='module')
def create_folders():
    """Create folders before test"""
    basedir = Path('testlibrary').absolute()
    paths = ['folder1/file1.txt',
             'folder2/folder21/file2.txt',
             'empptyfolder/emptyfolder11/',
             'emptyfolder2',
             'file3.txt',
             'folder4/file4.TXT',
             'folder5/incorrectfile.aaa']
    for path in paths:
        # if it is just directory
        if '.' not in path:
            Path(basedir).joinpath(path).mkdir(parents=True, exist_ok=True)
        else:
            #if it is file create directories first
            Path(basedir).joinpath(path).parent.mkdir(parents=True, exist_ok=True)
            Path(basedir).joinpath(path).touch()
    yield basedir
    shutil.rmtree(basedir)


def test__isformat():
    files = ['a.txt', 'a.TXT', 'a.Txt']
    for f in files:
        assert scanner._isformat(f, ['txt']) is True

    files = ['a.aaa', 'txt', 'aTXT', 'txt.a']
    for f in files:
        assert scanner._isformat(f, ['txt']) is False


def test_folders_scanner(create_folders):
    basedir = create_folders
    formats = ['txt']
    scan_result = [(str(basedir.joinpath('folder1')), 'file1.txt',),
                   (str(basedir.joinpath('folder2/folder21')), 'file2.txt',),
                   (str(basedir), 'file3.txt',),
                   (str(basedir.joinpath('folder4')), 'file4.TXT',)]
    assert set(scan_result) == set(scanner.scan(str(basedir), formats))


