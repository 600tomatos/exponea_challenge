from flask_restx._http import HTTPStatus


def make_error_response(errstr, code=HTTPStatus.BAD_REQUEST):
    """Create error response"""

    return ({'error': errstr}, code)


def build_response(data, code=HTTPStatus.OK):
    """Create ok response"""

    return (data, code)
