import shutil
from pathlib import Path
import pytest
from discogs_search.musiclibrary.scanner import Scanner


@pytest.fixture(scope='module')
def create_folders():
    """Create folders before test"""
    basedir = Path('testlibrary').absolute()
    paths = ['artist1/1950 album1/song1.mp3',
             'somefolder/artist1/1950 album2/song2.mp3',
             'empptyfolder/emptyfolder11/',
             'emptyfolder2',
             'file3.txt',
             '1950 album/song.mp3',
             'some/deep/folder/111 artist/1950 album/somefile.aaa']
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



def test_scan_folder(create_folders):
    basedir = create_folders
    sc = Scanner(str(basedir), '%A/%Y %a')
    scan_result = [{'artist': 'artist1', 'year': '1950', 'album': 'album1'},
                   {'artist': 'artist1', 'year': '1950', 'album': 'album2'},
                   {'artist': '111 artist', 'year': '1950', 'album': 'album'}]

    assert scan_result.sort(key=lambda x: x['artist']) == list(sc.scan()).sort(key=lambda x: x['artist'])


