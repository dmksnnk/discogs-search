import logging
from tinydb import TinyDB, Query, where
from discogs_search.musiclibrary.scanner import Scanner
from discogs_search.client import DiscogsClient
import config
from difflib import SequenceMatcher

logging.basicConfig(level=logging.INFO)
logging.getLogger('urllib3.connectionpool').propagate = False

logger = logging.getLogger('TestRun')

def is_equal(name1, name2):
    ratio = SequenceMatcher(None, name1.lower(), name2.lower()).quick_ratio()
    logger.debug('Match ratio for "%s" and "%s" is %.2f', name1, name2, ratio)
    if ratio  > 0.7:
        return True
    else:
        return False


db = TinyDB('test.json')
if len(db) == 0: # if database is empty
    # scan folder
    for album_data in Scanner('/media/Data/Music/', '%A/%Y - %a').scan():
        logger.debug(album_data)
        db.insert(album_data)


client = DiscogsClient(config.USER_AGENT, config.TOKEN)
missed_albums_db = TinyDB('missed_albums.json')
# get unique artists
artists = {album_data['artist'] for album_data in iter(db)}
# for artist in list(artists)[:10]:
for artist in artists:
    try:
        artist_results = client.search_artist(artist)
    except DiscogsClient.RequestFailedError as e:
        # TODO: try do request again
        logger.error(e)
        continue

    if not artist_results:
        logger.warning('Can\'t find {}'.format(artist))
        continue

    # first artist is the most similar to what we are searching for
    artist_id = artist_results[0]['id']
    try:
        releases = client.get_releases(artist_id)
    except DiscogsClient.RequestFailedError as e:
        # TODO: try do request again
        logger.error(e)
        continue
    # get only `Main` releases, not interested in `TrackAppearance`
    discogs_main_releases = [release for release in releases if release['role'] == 'Main']
    # albums of artist
    local_albums = [album_data['album'] for album_data in db.search(where('artist') == artist)]
    # comparing
    for discogs_release in discogs_main_releases:
        discogs_title = discogs_release['title']
        # if found in local albums - mark as found
        if any(is_equal(album, discogs_title) for album in local_albums):
            logger.info('++: {} - {}'.format(artist, discogs_title))
        else:
            logger.info('--: {} - {}'.format(artist, discogs_title))
            missed_albums_db.insert(discogs_release)

# print(missed_albums)


