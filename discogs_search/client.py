import logging
import time
import requests

logger = logging.getLogger('client')


class DiscogsClient():
    class RequestFailedError(Exception):
        def _init__(self, params, code):
            self.params = params
            self.code = code

        def __repr__(self):
            return 'Request with params {} failed ({})'.format(
                    self.params, self.code)


    def __init__(self, name, token):
        self.name = name
        self._token = token

    def search_artist(self, artist):
        search_result = self._search(artist, type='artist')
        return  search_result.get('results')

    def get_releases(self, artist_id):
        """Get releases for given artist id.

        :param artist_id: Artist id, can be found using ``search_artist``
        or on discogs page
        :type artist_id: int
        :returns: list of releases or None
        :rtype: list or None
        """
        url = 'https://api.discogs.com/artists/{}/releases'.format(artist_id)
        releases = self._get_request(url)
        return releases.get('releases')

    def _search(self, req, type):
        params = {'q': req,
                  'type': type}
        return self._get_request('https://api.discogs.com/database/search', params)

    def _get_request(self, url, params=None):
        """Sends GET request to URL.
        Checks for Ratelimit, if reach - waits for Retry-After seconds.
        """
        logger.debug('Sending request to %s with params %s', url, params)
        headers = {'user-agent': self.name}
        # if params aren't set
        if params is None:
            params = {'token': self._token}
        elif 'token' not in params.keys():
            params.update({'token': self._token})

        resp = requests.get(url, headers=headers, params=params)
        logger.debug('Receive response code %s, remaining %s requests',
                     resp.status_code, resp.headers.get('X-Discogs-Ratelimit-Remaining'))

        if resp.status_code not in [200, 204, 429]:
            raise self.RequestFailedError(params, resp.status_code)


        rate_limit = resp.headers.get('X-Discogs-Ratelimit-Remaining')
        if rate_limit and int(rate_limit) <= 1:
            retry_time = resp.headers.get('Retry-After')
            if retry_time:
                retry_time = int(retry_time)
                logger.warning('Reach Ratelimit, waiting for %s s', retry_time)
                time.sleep(retry_time)
            else:
                logger.error('Did not get Retry-After time')


        try:
            return resp.json()
        except ValueError:
            return {}
