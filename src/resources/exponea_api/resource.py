from flask_restx import Namespace
from flask_restx._http import HTTPStatus

from interfaces.resource import ResourceItf

from serde.models import response_model
from serde.parsers import request_parser
from services.exponea_api import ExponeaApiService

ns = Namespace('Exponea API', description='Various types of requests to the Exponea server', path='/')


@ns.route('/all')
@ns.expect(request_parser)
@ns.doc(responses={
    HTTPStatus.OK: 'Ok',
    HTTPStatus.BAD_REQUEST: 'Bad request',
    HTTPStatus.INTERNAL_SERVER_ERROR: 'Unexpected response',
})
class CollectAllSuccessRespView(ResourceItf):
    # Base service (Business logic layer)
    service = ExponeaApiService()

    @ns.response(code=HTTPStatus.OK, model=[response_model], description='List of all responses')
    def get(self):
        """
        Collects all successful responses from Exponea testing HTTP server and
        returns the result as an array. If timeout is reached before all requests finish, or none of
        the responses were successful, the endpoint should return an error.
        """

        return self.service.all()

    # # @ns.response(code=HTTPStatus.OK, model=[list_announcement_model], description='List of all announcements')
    # def get(self):
    #     """List of all announcements"""
    #
    #     return self.service.list()


@ns.route('/first')
@ns.expect(request_parser)
@ns.doc(responses={
    HTTPStatus.OK: 'Ok',
    HTTPStatus.BAD_REQUEST: 'Bad request',
    HTTPStatus.INTERNAL_SERVER_ERROR: 'Unexpected response',
})
class CollectFirstSuccessRespView(ResourceItf):
    # Base service (Business logic layer)
    service = ExponeaApiService()

    @ns.response(code=HTTPStatus.OK, model=[response_model], description='First successfull response')
    def get(self):
        """
        Returns the first successful response that returns from Exponea testing
        HTTP server. If timeout is reached before any successful response was received, the
        endpoint should return an error.
        """

        return self.service.first()


@ns.route('/within-timeout')
@ns.expect(request_parser)
@ns.doc(responses={
    HTTPStatus.OK: 'Ok',
    HTTPStatus.BAD_REQUEST: 'Bad request',
    HTTPStatus.INTERNAL_SERVER_ERROR: 'Unexpected response',
})
class CollectSuccessRespWithinRequestView(ResourceItf):
    # Base service (Business logic layer)
    service = ExponeaApiService()

    @ns.response(code=HTTPStatus.OK, model=[response_model], description='All successfull responses within timeout.')
    def get(self):
        """
        Collects all successful responses that return within a given
        timeout. If a timeout is reached before any of the 3 requests finish, the server should
        return an empty array instead of an error. (This means that this endpoint should never
        return an error).
        """

        return self.service.within_timeout()


@ns.route('/smart')
@ns.expect(request_parser)
@ns.doc(responses={
    HTTPStatus.OK: 'Ok',
    HTTPStatus.BAD_REQUEST: 'Bad request',
    HTTPStatus.INTERNAL_SERVER_ERROR: 'Unexpected response',
})
class CollectSuccessRespSmartRequestView(ResourceItf):
    # Base service (Business logic layer)
    service = ExponeaApiService()

    @ns.response(code=HTTPStatus.OK, model=response_model, description='Smart request.')
    def get(self):
        """
        instead of firing all 3 requests at once, this endpoint will first fire
        only a single request to Exponea testing HTTP server. Then 2 scenarios can happen:
        a. Received a successful response within 300 milliseconds: return the response
        b. Didn’t receive a response within 300 milliseconds, or the response was not
        successful: fire another 2 requests to Exponea testing HTTP server. Return the
        first successful response from any of those 3 requests (including the first one).
        """

        return self.service.smart()
