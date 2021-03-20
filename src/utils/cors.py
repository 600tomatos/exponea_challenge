from flask import request, make_response, jsonify


def CORS(app):
    """
    Apply CORS policies to an app.
    """

    @app.before_request
    def before_request():
        """
        Answer directly all OPTIONS requests to improve performance and
        also to cache it on the requester.

        It was used as a solution to the app "getting stuck", probably because
        of CORS preflight calls.
        """
        if request.method == "OPTIONS":
            response = make_response(jsonify(None), 204)
            response.headers = {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Max-Age": "1728000",
            }
            return response

    return app
