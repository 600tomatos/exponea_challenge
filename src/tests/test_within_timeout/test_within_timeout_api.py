import time
import pytest


class TestWithinTimeoutApiSuite:
    _base_url_preffix = 'api/within-timeout'

    @pytest.mark.parametrize('timeout', [
        1,
        3,
        2000,
        4000,
        '6000',
        '7000',
    ])
    def test_ok(self, app, timeout):
        with app.test_client() as client:
            res = client.get(f'{self._base_url_preffix}?timeout={timeout}')

            code = res.status_code
            assert code == 200

            payload = res.json
            assert isinstance(payload, list)
            assert 0 <= len(payload) < 4
            # All items contain time key
            assert all(set(i.keys() == {'time', } for i in payload))

    @pytest.mark.parametrize('timeout, error', [
        (0, 'Only positive values of integer or float are acceptable for timeout'),
        (-100, 'Only positive values of integer or float are acceptable for timeout'),
        ('abcd', 'Timeout can be a string, but the string represent a valid number. Your value is not valid'),
        ('40!!00', 'Timeout can be a string, but the string represent a valid number. Your value is not valid'),
        (None, 'Timeout can be a string, but the string represent a valid number. Your value is not valid'),
        (True, 'Timeout can be a string, but the string represent a valid number. Your value is not valid'),
        (False, 'Timeout can be a string, but the string represent a valid number. Your value is not valid'),
    ])
    def test_invalid_timeout(self, app, timeout, error):
        with app.test_client() as client:
            res = client.get(f'{self._base_url_preffix}?timeout={timeout}')

            code = res.status_code
            assert code == 400

            assert res.json['error'] == error

    @pytest.mark.parametrize('timeout', [
        2000,
        4000,
        7000,
        8000,
    ])
    def test_timeout_is_in_bounds(self, app, timeout):
        """Check if execution time approximately equal to timeout"""

        # convert miliseconds to seconds
        timeout_sec = timeout / 1e3
        now = time.time()

        with app.test_client() as client:
            client.get(f'{self._base_url_preffix}?timeout={timeout}')

        exec_time = time.time() - now
        assert int(exec_time) <= timeout_sec
