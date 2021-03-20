import logging
import requests

logger = logging.getLogger(__name__)


class Response:
    """Internal response object"""

    def __init__(self, result, url):
        self.result = result
        self.url = url

        self._handle_status_code()

    @property
    def OK(self):
        return 200 <= self.status_code < 400

    @property
    def NOT_OK(self):
        return not self.OK

    @property
    def status_code(self):
        return self.result.status_code

    @property
    def json(self):
        return self.result.json()

    def _handle_status_code(self):
        if self.NOT_OK:
            try:
                error = self.json
            except:
                error = f'{self.result.raw} | {self.result.reason}'
            logger.warning('************************************************************************')
            logger.warning(f'Error while requesting to url {self.url} '
                           f'Status code: {self.status_code}. '
                           f'Reason: {error}')
            logger.warning('************************************************************************')


class ApiClient:
    """
        Client for requests to API. Only get and post methods are present for simplicity
    """

    def __init__(self, base_url, loop):
        self.base_url = base_url
        self.loop = loop

    async def get(self):
        response = await self.loop.run_in_executor(None, requests.get, self.base_url)
        return Response(response, self.base_url)

    async def post(self):
        response = await self.loop.run_in_executor(None, requests.post, self.base_url)
        return Response(response, self.base_url)
