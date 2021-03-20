import time
import requests

from multiprocessing import Process, Queue


class TestFirstConcurrencySuite:
    q = Queue()
    _base_url_preffix = 'api/first'

    def test_concurrency(self, base_url, multiproc_event, parallel_procs_num, executor_timeout):
        """
        The test involves multiple calls to the endpoint.

        """

        # Start n number of independent processes
        _range = list(range(parallel_procs_num))
        for _ in _range:
            Process(target=self._make_request,
                    args=(base_url, self.q, multiproc_event),
                    daemon=True).start()

        now = time.time()

        timeout = now + executor_timeout

        while now < timeout:
            now = time.time()

            try:
                res, code = self.q.get(timeout=3)
            except Exception as e:
                multiproc_event.set()
                assert not e, 'Unable to make requests'
                return

            assert code in (200, 400)

            if code == 200:
                assert set(res.keys()) == {'time', }
            else:

                assert res['error'] in (
                    'Remote server request expirienced timeout',
                    'One or more requests were unsuccessful',
                    'All responses were unsuccessful'
                )
        if not multiproc_event.is_set():
            multiproc_event.set()

    def _make_request(self, base_url, queue, event):

        while not event.is_set():
            res = requests.get(f'{base_url}/{self._base_url_preffix}?timeout=2000')

            status_code = res.status_code
            data = res.json()
            queue.put_nowait((data, status_code))
