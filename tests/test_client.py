from unittest.mock import patch
from discogs_client import DiscogsClient
from config import USER_AGENT, TOKEN


def test_init_client(client):
    assert client.name == USER_AGENT
    assert client._token == TOKEN


@patch.object(DiscogsClient, '_search')
def test_find_artist_call__search(mock__search, client):
    client.search_artist('kyuss')
    mock__search.assert_called_with('kyuss', type='artist')


@patch.object(DiscogsClient, '_get')
def test_find_artist_returns_artist_data(mock__get, client, search_results, artists):
    mock__get.return_value = search_results

    artist_data = client.search_artist('kyuss')
    assert artist_data == artists


@patch.object(DiscogsClient, '_get')
def test_find_artist_returns_empty_data(mock__get, client):
    mock__get.return_value = {'results': []}

    artist_data = client.search_artist('kyuss')
    assert artist_data == []


@patch.object(DiscogsClient, '_get')
def test_get_releases(mock__get, client, releases_results, releases):
    mock__get.return_value = releases_results

    artist_id = 105732
    assert client.get_artist_releases(artist_id) == releases