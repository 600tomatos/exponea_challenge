import os
import time
import asyncio
import logging

from concurrent.futures._base import TimeoutError

from flask_restx import marshal

from interfaces.service import ServiceItf
from utils.response import (
    make_error_response
)
from serde.models import response_model
from utils.api_client import ApiClient
from validators.timeout_validator import TimeoutValidator

logger = logging.getLogger()

REQUESTS_COUNT = 3
TIMEOUT_MARK = 'x'

# This url should come from env but I left default value for test purposes
URL = os.getenv('EXPONEA_URL', 'https://exponea-engineering-assignment.appspot.com/api/work')


class ExponeaApiService(ServiceItf):
    """All services use standard consumer/producer approach to handle multi responses from third part API"""

    # Validators chain before endpoint execution
    validators = [TimeoutValidator]

    async def all(self, request):
        """
        Collects all successful responses from Exponea testing HTTP server and
        returns the result as an array. If timeout is reached before all requests finish, or none of
        the responses were successful, the endpoint should return an error.
        """

        timeout = int(request.args['timeout'])

        loop = request.get_loop()
        api_client = ApiClient(URL, loop)
        response_collector = asyncio.Queue()

        # convert miliseconds to seconds
        timeout_sec = timeout / 1e3

        logger.info(f'Provided timeout in seconds = {timeout_sec}')

        # Start producers in background
        producers_job = loop.create_task(
            self._start_all_producers(api_client, response_collector, timeout_sec))

        result_list = []
        async for resp in self._consume_responses(queue=response_collector, timeout=timeout_sec):
            if resp:
                if resp != TIMEOUT_MARK:
                    # Store successfull responses
                    result_list.append(resp)
                else:
                    producers_job.cancel()
                    return make_error_response('Remote server request expirienced timeout')
            else:
                return make_error_response('One or more requests were unsuccessful')

        return marshal(result_list, response_model)

    async def first(self, request):
        """
        Returns the first successful response that returns from Exponea testing
        HTTP server. If timeout is reached before any successful response was received, the
        endpoint should return an error.
        """

        timeout = int(request.args['timeout'])

        loop = request.get_loop()
        api_client = ApiClient(URL, loop)
        response_collector = asyncio.Queue()

        # convert miliseconds to seconds
        timeout_sec = timeout / 1e3

        logger.info(f'Provided timeout in seconds = {timeout_sec}')

        # Start producers in background
        producers_job = loop.create_task(
            self._start_all_producers(api_client, response_collector, timeout_sec))

        cycles = 0
        async for resp in self._consume_responses(queue=response_collector, timeout=timeout_sec):
            if resp:
                if resp != TIMEOUT_MARK:
                    # Return successfull response
                    producers_job.cancel()
                    return marshal(resp, response_model)
                else:
                    producers_job.cancel()
                    return make_error_response('Remote server request expirienced timeout')
            cycles += 1
            if cycles == REQUESTS_COUNT:
                return make_error_response('All responses were unsuccessful')

    async def within_timeout(self, request):

        """
        Collects all successful responses that return within a given
        timeout. If a timeout is reached before any of the 3 requests finish, the server should
        return an empty array instead of an error. (This means that this endpoint should never
        return an error).
        """

        timeout = int(request.args['timeout'])

        loop = request.get_loop()
        api_client = ApiClient(URL, loop)
        response_collector = asyncio.Queue()

        # convert miliseconds to seconds
        timeout_sec = timeout / 1e3

        logger.info(f'Provided timeout in seconds = {timeout_sec}')

        # Start producers in background
        producers_job = loop.create_task(
            self._start_all_producers(api_client, response_collector, timeout_sec))

        result_list = []
        cycles = 0
        async for resp in self._consume_responses(queue=response_collector, timeout=timeout_sec):
            if resp and resp != TIMEOUT_MARK:
                result_list.append(resp)
            cycles += 1
            if cycles == REQUESTS_COUNT:
                break

        producers_job.cancel()
        return marshal(result_list, response_model)

    async def smart(self, request):

        """
        instead of firing all 3 requests at once, this endpoint will first fire
        only a single request to Exponea testing HTTP server. Then 2 scenarios can happen:
        a. Received a successful response within 300 milliseconds: return the response
        b. Didn’t receive a response within 300 milliseconds, or the response was not
        successful: fire another 2 requests to Exponea testing HTTP server. Return the
        first successful response from any of those 3 requests (including the first one).
        """

        timeout = int(request.args['timeout'])

        loop = request.get_loop()
        api_client = ApiClient(URL, loop)
        response_collector = asyncio.Queue()

        # convert miliseconds to seconds
        timeout_sec = timeout / 1e3

        # Timeout for first 'smart' attempt
        first_timeout_sec = .3
        total_producers_count = REQUESTS_COUNT - 1

        logger.info(f'Provided timeout in seconds = {timeout_sec}')

        # Start first producer
        loop.create_task(self._produce_request(api_client, response_collector, first_timeout_sec, 1))
        resp = await self._consume_response(response_collector, first_timeout_sec)
        if resp != TIMEOUT_MARK:
            return marshal(resp, response_model)

        # Start producers in background
        producers_job = loop.create_task(
            self._start_all_producers(api_client,
                                      response_collector,
                                      timeout_sec,
                                      producers_total_count=total_producers_count))

        cycles = 0
        async for resp in self._consume_responses(queue=response_collector, timeout=timeout_sec):
            if resp:
                if resp != TIMEOUT_MARK:
                    # Return successfull response
                    producers_job.cancel()
                    return marshal(resp, response_model)
                else:
                    producers_job.cancel()
                    return make_error_response('Remote server request expirienced timeout')
            cycles += 1
            if cycles == total_producers_count:
                return make_error_response('All responses were unsuccessful')

    # ------------------------------------------------------------------------------------------------------------------
    #                               Auxilary methods
    # ------------------------------------------------------------------------------------------------------------------

    async def _consume_response(self, queue, timeout):
        try:
            data = await asyncio.wait_for(queue.get(), timeout=timeout)
            return data
        except TimeoutError:
            return TIMEOUT_MARK

    async def _consume_responses(self, queue, timeout):
        """Async generator with timeout calculation"""

        for _ in range(REQUESTS_COUNT):
            start_at = time.monotonic()

            data = await self._consume_response(queue, timeout)
            yield data

            # subtract the time of request from the timeout
            timeout -= time.monotonic() - start_at

    async def _produce_request(self, api_client, queue, timeout, producer_num):

        logger.info(f'Producer {producer_num} started..')
        response = await api_client.get()

        logger.info(f'Producer {producer_num} finished')
        if response.OK:
            queue.put_nowait(response.json)
        else:
            # Status code != 200
            queue.put_nowait(None)

    async def _start_all_producers(self, api_client, queue, timeout, producers_total_count=REQUESTS_COUNT):
        """Start all requests at once"""

        tasks = [self._produce_request(api_client, queue, timeout, i + 1) for i in range(producers_total_count)]
        await asyncio.gather(*tasks)
