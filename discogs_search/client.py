import requests

class DiscogsClient():
    def __init__(self, name, token):
        self.name = name
        self._token = token

    def search_artist(self, artist):
        search_result = self._search(artist, type='artist')
        return  search_result.get('results')

    def get_artist_releases(self, artist_id):
        """Get releases for given artist id.

        :param artist_id: Artist id, can be found using ``search_artist``
        or on discogs page
        :type artist_id: int
        :returns: list of releases or None
        :rtype: list or None
        """
        url = 'https://api.discogs.com/artists/{}/releases'.format(artist_id)
        releases = self._get(url)
        return releases.get('releases')

    def _search(self, req, type):
        params = {'q': req,
                  'type': type}
        return self._get('https://api.discogs.com/database/search', params)

    def _get(self, url, params=None):
        headers = {'user-agent': self.name}
        # if params aren't set
        if params is None:
            params = {'token': self._token}
        elif 'token' not in params.keys():
            params.update({'token': self._token})

        resp = requests.get(url, headers=headers, params=params)
        try:
            return  resp.json()
        except ValueError:
            return None
