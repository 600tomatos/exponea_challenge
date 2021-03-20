from flask_restx import Model, fields

response_model = Model('ResponseModel', {
    'time': fields.Integer(required=True, example=600)
})
