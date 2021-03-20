import logging
import asyncio
from abc import ABC

from flask import request as base_request

from types import SimpleNamespace

from utils.response import make_error_response

logger = logging.getLogger()


class AdaptiveNamespace(SimpleNamespace):

    def __getattr__(self, item):
        """get any attribute from request"""

        return getattr(base_request, item)


class ServiceItf(ABC):
    """Base service interface for business logic tasks"""

    # Default validators for common logic across all service methods
    validators = []

    def __new__(cls, *args, **kwargs):

        cls._apply_decorator_to_methods(cls._flow_control)
        self = super().__new__(cls)
        return self

    def __init__(self):
        self._request = None

    @classmethod
    def _apply_decorator_to_methods(cls, decorator):
        """
        This helper can apply a given decorator to all methods on the current
        Resource.
        """

        for method in cls._methods():
            method_name = method.lower()
            decorated_method_func = decorator(getattr(cls, method_name))
            setattr(cls, method_name, decorated_method_func)

    @classmethod
    def _methods(cls):
        """All service methods"""

        return [func for func in dir(cls) if callable(getattr(cls, func)) and not func.startswith('_')]

    @classmethod
    def _flow_control(cls, service_method):
        """
        The default decorator for each instance of the service.
        The task of this decorator is to make the call of synchronous and asynchronous methods universal
        """

        def __wrapper(self, *args, **kwargs):
            # build request wrapper over original request

            request = cls._build_request()

            # Apply default validators
            for validator in cls.validators:
                error = validator.check(request)
                if error:
                    logger.error(str(error))
                    # If a validation error occurs,
                    # then return an error in response without executing a handler for this endpoint
                    return make_error_response(error)

            response = service_method(self, request)

            if asyncio.iscoroutine(response):
                response = asyncio.run(response)

            return response

        return __wrapper

    @classmethod
    def _build_request(self):
        """Build request wrapper"""

        request = AdaptiveNamespace()

        # Create Thread adaptive event loop
        get_loop = lambda: asyncio.get_event_loop()
        request.get_loop = get_loop

        return request
