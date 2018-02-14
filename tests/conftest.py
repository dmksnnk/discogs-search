import pytest
from discogs_search import DiscogsClient
from config import TOKEN, USER_AGENT


_search_results = {'pagination':
                       {'per_page': 50,
                        'items': 53,
                        'page': 1,
                        'urls':
                            {'last': 'https://api.discogs.com/database/search?q=kyuss&per_page=50&token=SnlTMGMAzKlTXhTKfZvBrfzTtrQvEIykxMrzSZQr&type=artist&page=2',
                             'next': 'https://api.discogs.com/database/search?q=kyuss&per_page=50&token=SnlTMGMAzKlTXhTKfZvBrfzTtrQvEIykxMrzSZQr&type=artist&page=2'},
                        'pages': 2},
                   'results': [
                       {'thumb': 'https://img.discogs.com/AvScxAvezy-nwdksAbCdbg7mAS8=/150x150/smart/filters:strip_icc():format(jpeg):mode_rgb():quality(40)/discogs-images/A-105732-1105959007.jpg.jpg',
                        'title': 'Kyuss',
                        'uri': '/artist/105732-Kyuss',
                        'resource_url': 'https://api.discogs.com/artists/105732',
                        'type': 'artist',
                        'id': 105732},
                       {'thumb': '',
                        'title': 'Kyuss Lives!',
                        'uri': '/artist/5809616-Kyuss-Lives!',
                        'resource_url': 'https://api.discogs.com/artists/5809616',
                        'type': 'artist',
                        'id': 5809616}
                   ]}


_releases = {'pagination':
                {'per_page': 50,
                 'items': 90,
                 'page': 1,
                 'urls':
                     {'last': 'https://api.discogs.com/artists/105732/releases?per_page=50&token=SnlTMGMAzKlTXhTKfZvBrfzTtrQvEIykxMrzSZQr&page=2',
                      'next': 'https://api.discogs.com/artists/105732/releases?per_page=50&token=SnlTMGMAzKlTXhTKfZvBrfzTtrQvEIykxMrzSZQr&page=2'},
                 'pages': 2},
            'releases': [
                {'thumb': 'https://img.discogs.com/BuTeKG4H8NuewFHY6_3ubfZPiYo=/fit-in/150x150/filters:strip_icc():format(jpeg):mode_rgb():quality(40)/discogs-images/R-1737819-1264586426.jpeg.jpg',
                 'artist': 'Sons Of Kyuss*',
                 'main_release': 1737819,
                 'title': 'Sons Of Kyuss',
                 'role': 'Main',
                 'year': 1990,
                 'resource_url': 'https://api.discogs.com/masters/105488',
                 'type': 'master',
                 'id': 105488},
                {'thumb': 'https://img.discogs.com/2krCKx5NYDz3WSBvjrzgbLlXAYM=/fit-in/150x150/filters:strip_icc():format(jpeg):mode_rgb():quality(40)/discogs-images/R-370733-1122546954.jpg.jpg',
                 'artist': 'Kyuss',
                 'main_release': 370733,
                 'title': 'Wretch',
                 'role': 'Main',
                 'year': 1991,
                 'resource_url': 'https://api.discogs.com/masters/54030',
                 'type': 'master',
                 'id': 54030},
                {'status': 'Accepted',
                 'thumb': 'https://img.discogs.com/QLETQjQwfu0_n6QXJ3_yoGggFik=/fit-in/150x150/filters:strip_icc():format(jpeg):mode_rgb():quality(40)/discogs-images/R-3033833-1312642860.jpeg.jpg',
                 'title': 'Thong Song',
                 'format': 'CD, Single, Promo',
                 'label': 'Dali Records',
                 'role': 'Main',
                 'year': 1992,
                 'resource_url': 'https://api.discogs.com/releases/3033833',
                 'artist': 'Kyuss',
                 'type':'release',
                 'id': 3033833}
                ]
}


@pytest.fixture(scope='module')
def client():
    return DiscogsClient(name=USER_AGENT, token=TOKEN)


@pytest.fixture(scope='module')
def search_results():
    return _search_results


@pytest.fixture(scope='module')
def artists(search_results):
    return search_results['results']


@pytest.fixture(scope='module')
def releases_results():
    return _releases


@pytest.fixture(scope='module')
def releases():
    return _releases['releases']