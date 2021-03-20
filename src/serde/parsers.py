from flask_restx import reqparse

request_parser = reqparse.RequestParser()
request_parser.add_argument('timeout', location='args', type=int, nullable=False, required=True,
                            help='Request timeout in miliseconds.', default=3000)
