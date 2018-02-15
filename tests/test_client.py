from unittest.mock import patch, Mock
import pytest
from discogs_search import DiscogsClient
from config import USER_AGENT, TOKEN

@pytest.fixture()
def response():
    resp = Mock(['status_code', 'headers', 'json'])
    return resp


@pytest.fixture()
def response_ok(response):
    response.status_code = 200
    response.headers = {'X-Discogs-Ratelimit-Remaining': '60',
                        'X-Discogs-Ratelimit-Used': '1',
                        'X-Discogs-Ratelimit': '60'}
    response.json.return_value = 'somedata'
    return response


@pytest.fixture()
def response_at_ratelimit(response):
    response.status_code = 429
    response.headers = {'X-Discogs-Ratelimit-Remaining': '1',
                        'X-Discogs-Ratelimit-Used': '60',
                        'X-Discogs-Ratelimit': '60',
                        'Retry-After': '60'}
    response.json.return_value = 'somedata'
    return response


def test_init_client(client):
    assert client.name == USER_AGENT
    assert client._token == TOKEN


@patch('requests.get')
def test__get_request_adds_user_agent_and_token(mock_get, client, response_ok):
    mock_get.return_value = response_ok
    headers = {'user-agent': USER_AGENT}
    params = {'token': TOKEN}

    client._get_request('someurl')
    mock_get.assert_called_with('someurl', headers=headers, params=params)


@patch('requests.get')
def test__get_request_on_response_200(mock_get, client, response_ok):
    mock_get.return_value = response_ok

    data = client._get_request('someurl')
    assert data == 'somedata'


@patch('requests.get')
def test__get_request_on_response_400(mock_get, client, response_ok):
    response_ok.status_code = 400
    mock_get.return_value = response_ok

    with pytest.raises(client.RequestFailedError) as e:
        client._get_request('someurl')
    assert 400 in e.value.args


@patch('time.sleep')
@patch('requests.get')
def test__get_request_sleeps_on_reach_ratelimit(mock_get, mock_sleep, client, response_at_ratelimit):
    mock_get.return_value = response_at_ratelimit

    data = client._get_request('someurl')
    mock_sleep.assert_called_with(60)
    assert data == 'somedata'


@patch('time.sleep')
@patch('requests.get')
def test__get_request_on_reach_ratelimit_but_no_retry_time(mock_get, mock_sleep, client, response_at_ratelimit):
    response_at_ratelimit.headers.pop('Retry-After')
    mock_get.return_value = response_at_ratelimit

    data = client._get_request('someurl')
    mock_sleep.assert_not_called()
    assert data == 'somedata'


# ---- testing search ------
@patch.object(DiscogsClient, '_search')
def test_find_artist_call__search(mock__search, client):
    client.search_artist('kyuss')
    mock__search.assert_called_with('kyuss', type='artist')


@patch.object(DiscogsClient, '_get_request')
def test_search_artist_returns_artist_data(mock__get_request, client, search_results, artists):
    mock__get_request.return_value = search_results

    artist_data = client.search_artist('kyuss')
    assert artist_data == artists


@patch.object(DiscogsClient, '_get_request')
def test_search_artist_returns_empty_data(mock__get_request, client):
    mock__get_request.return_value = {'results': []}

    artist_data = client.search_artist('kyuss')
    assert artist_data == []


@patch.object(DiscogsClient, '_get_request')
def test_get_artist_releases(mock__get_request, client, releases_results, releases):
    mock__get_request.return_value = releases_results

    artist_id = 105732
    assert client.get_artist_releases(artist_id) == releases
