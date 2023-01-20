

import geocoder
import requests_cache

import requests
from operator import itemgetter


session = requests_cache.CachedSession(
    'api_cache',
    # Save files in the default user cache dir
    use_cache_dir=True,
    # Don't match this param or save it in the cache
    ignored_parameters=['request', 'terms'],
    # In case of request errors, use stale cache data if possible
    stale_if_error=True,
)


def get_city_by_iata_code(api_key, api_url, iata_codes=[]):
    result = {'iata_codes': {}, 'error': ''}

    try:
        raw_res = session.get(api_url, params={
            'api_key': api_key, 'iata_code': iata_codes})
    except requests.exceptions.RequestException:
        result['error'] = "Couldn't connect to the API"
        return result

    print("IS IT CACHE?", raw_res.from_cache)

    response = raw_res.json()
    if raw_res.status_code == 200 and 'error' not in response:
        for airport in response['response']:
            name, iata_code, lat, lng = itemgetter(
                'name', 'iata_code', 'lat', 'lng')(airport)

            try:
                g = geocoder.osm(
                    [lat, lng], method='reverse', lang_code="en-US")
                city, country = itemgetter('state', 'country')(g.json)
            except TypeError:
                result['error'] = "Couldn't get city from coordinates."
                return result

            result['iata_codes'][iata_code] = {
                'name': name,
                'city': city,
                'country': country,
            }

    else:
        result['error'] = response['error']['message']

    return result
